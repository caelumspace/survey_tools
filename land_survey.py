import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.geometry as geom
import ezdxf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv
import json
import math
import argparse

# Function to convert lat/lon to UTM
def latlon_to_utm(lat, lon):
    from pyproj import Proj
    utm_proj = Proj(proj="utm", zone=math.floor((lon + 180) / 6) + 1, ellps="WGS84")
    return utm_proj(lon, lat)

# Function to compute distance and bearing
def compute_meets_bounds(coords):
    meets_bounds = []
    for i in range(len(coords)):
        p1, p2 = coords[i], coords[(i + 1) % len(coords)]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        distance = math.sqrt(dx**2 + dy**2)
        bearing = math.degrees(math.atan2(dy, dx)) % 360
        meets_bounds.append((p1, p2, distance, bearing))
    return meets_bounds

# Convert bearing to quadrant bearing string
def bearing_to_quadrant(bearing_deg):
    if 0 <= bearing_deg < 90:
        return f"North {bearing_deg:.2f}° East"
    elif 90 <= bearing_deg < 180:
        return f"South {180 - bearing_deg:.2f}° East"
    elif 180 <= bearing_deg < 270:
        return f"South {bearing_deg - 180:.2f}° West"
    else:
        return f"North {360 - bearing_deg:.2f}° West"

# Generate formal meets and bounds legal description
def generate_meets_bounds_description(meets_bounds):
    description = "Beginning at a point located at the coordinates " \
                  f"{meets_bounds[0][0][0]:.2f}, {meets_bounds[0][0][1]:.2f};\n"
    for _, p2, distance, bearing in meets_bounds:
        quadrant = bearing_to_quadrant(bearing)
        description += f"thence {quadrant}, a distance of {distance:.2f} feet to a point;\n"
    description += "Returning to the point of beginning.\n"
    return description

# Function to generate DXF survey map
def generate_dxf(coords, filename="survey.dxf"):
    doc = ezdxf.new()
    msp = doc.modelspace()
    for i in range(len(coords)):
        p1, p2 = coords[i], coords[(i + 1) % len(coords)]
        msp.add_line(p1, p2)
    doc.saveas(filename)

# Function to generate PDF survey document
def generate_pdf(meets_bounds, filename="survey.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Land Survey Report")
    y = 720
    description = generate_meets_bounds_description(meets_bounds)
    for line in description.split("\n"):
        if y < 50:
            c.showPage()
            y = 750
            c.setFont("Helvetica", 12)
        c.drawString(100, y, line)
        y -= 20
    c.save()

# Create a sample CSV file
def create_sample_input(filename="survey_points.csv"):
    sample_data = [
        [1, 38.8951, -77.0364],
        [2, 38.8955, -77.0358],
        [3, 38.8948, -77.0355],
        [4, 38.8946, -77.0362],
    ]
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "lat", "lon"])
        writer.writerows(sample_data)
    print(f"Sample input file '{filename}' created.")

# Main function
def process_survey(input_file):
    coords = []
    with open(input_file, "r") as f:
        if input_file.endswith(".csv"):
            reader = csv.reader(f)
            next(reader)
            coords = [(float(row[1]), float(row[2])) for row in reader]
        elif input_file.endswith(".json"):
            data = json.load(f)
            coords = [(p["lat"], p["lon"]) for p in data["points"]]

    utm_coords = [latlon_to_utm(lat, lon) for lat, lon in coords]
    meets_bounds = compute_meets_bounds(utm_coords)
    generate_dxf(utm_coords)
    generate_pdf(meets_bounds)
    print("Survey document and map generated successfully.")

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a land survey document from GPS points.")
    parser.add_argument("--input", type=str, help="Input CSV or JSON file with survey points.")
    parser.add_argument("--sample", action="store_true", help="Create a sample survey_points.csv file and run it.")
    args = parser.parse_args()

    if args.sample:
        create_sample_input()
        process_survey("survey_points.csv")
    elif args.input:
        process_survey(args.input)
    else:
        print("Please specify --input <file> or use --sample to create and test with sample data.")
