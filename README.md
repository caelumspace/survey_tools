## Land Survey Generator

This is a Python-based tool to generate official-style **land survey documents** from:

- GPS tracks
  
- OpenStreetMap coordinates
  
- Google Maps pins
  
- CSV, JSON, KML, and GPX files
  

Outputs include:

- **Meets and Bounds legal description** (PDF)
  
- **Survey map** (DXF, AutoCAD-compatible)
  

---

### Features

- Accepts inputs from `.csv`, `.json`, `.kml`, `.gpx`
  
- Calculates distances and bearings between points
  
- Converts bearings to quadrant-based descriptions
  
- Outputs ready-to-submit land survey PDF & DXF
  
- Includes sample data generation for testing
  

---

### Dependencies

Install with:

```pip install geopandas shapely ezdxf reportlab fastkml matplotlib pyproj```

> Optional: For `.gpx` support, `lxml` and `xml.etree.ElementTree` are used (standard library + optional).

---

### Usage

#### Run with your own data:

`python land_survey.py --input my_points.csv
python land_survey.py --input field_recording.kml`

#### Create and use sample data:

`python land_survey.py --sample # Uses sample_points.csv python land_survey.py --sample-kml # Uses sample_points.kml`

---

### Input Formats

#### CSV

`id,lat,lon
1,38.8951,-77.0364
2,38.8955,-77.0358
...`

#### JSON

`{ "points": [ { "lat": 38.8951, "lon": -77.0364 }, { "lat": 38.8955, "lon": -77.0358 } ] }`

#### KML

Automatically parsed from `<coordinates>` tags.

#### GPX

Parsed from `<trkpt>` tags with lat/lon attributes.

---

### Output

- `survey.pdf` – formatted meets & bounds text
  
- `survey.dxf` – vector drawing of the parcel
  

---

### Example Output (PDF)


```Land Survey Report
Beginning at a point located at the coordinates 322345.55, 4299001.32;
thence North 45.00° East, a distance of 100.00 feet to a point;
...
Returning to the point of beginning.```

---

### Future Ideas

- Elevation support from GPX/KML
  
- Polygon closure validation
  
- Export to Word (DOCX)
  
- Digital signature & notary block
