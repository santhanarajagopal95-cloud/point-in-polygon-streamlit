
import json
from typing import List, Tuple

import streamlit as st
from shapely.geometry import Point, Polygon
from shapely.validation import explain_validity
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Point in Polygon Checker", page_icon="📍", layout="centered")

st.title("📍 Point in Polygon Checker")
st.caption("Enter a polygon and a point, then click Check to see whether the point lies inside the polygon. Supported formats: lon,lat lines or GeoJSON.")

# Sample inputs
sample_poly_lines = """79.3479688288648,10.98775809708549
79.32348738181935,11.005293262398226
79.30032934779183,10.980610758801461
79.30760632236604,10.913055003692932
79.3532614415277,10.870823079150227
79.41611903303561,10.880568878683093
79.4346410300393,10.954630465654162
79.4187629197537,10.987757360769919
79.3479688288648,10.98775809708549"""

sample_point = "79.37046033537382,10.960475479633104"

mode = st.radio("Polygon input mode", ["Lines (lon,lat per line)", "GeoJSON Polygon"], horizontal=True)

poly_text = st.text_area(
    "Polygon",
    value=sample_poly_lines.strip(),
    height=180,
    help="Lines mode: one 'lon,lat' per line. GeoJSON mode: paste a Polygon object."
)

point_text = st.text_input(
    "Point (lon,lat) or GeoJSON Point",
    value=sample_point,
    help="Example lon,lat: 79.37046,10.96047   or  GeoJSON: {\"type\":\"Point\",\"coordinates\":[79.37,10.96]}"
)

def parse_point(text: str) -> Tuple[float, float]:
    text = text.strip()
    # Try JSON first
    if text.startswith("{"):
        obj = json.loads(text)
        if obj.get("type") == "Point" and "coordinates" in obj:
            lon, lat = obj["coordinates"]
            return float(lon), float(lat)
        else:
            raise ValueError("GeoJSON must be a Point with 'coordinates'.")
    # Fallback to lon,lat
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 2:
        raise ValueError("Point must be 'lon,lat' or GeoJSON Point.")
    return float(parts[0]), float(parts[1])

def parse_polygon(text: str, mode: str) -> List[Tuple[float, float]]:
    text = text.strip()
    if mode == "GeoJSON Polygon":
        obj = json.loads(text)
        geom = obj.get("geometry") if obj.get("type") == "Feature" else obj
        if geom.get("type") != "Polygon":
            raise ValueError("GeoJSON must be of type 'Polygon'.")
        ring = geom.get("coordinates")[0]
        return [(float(x), float(y)) for x, y in ring]
    else:
        pts = []
        for ln in text.splitlines():
            ln = ln.strip()
            if not ln: 
                continue
            parts = [p.strip() for p in ln.split(",")]
            if len(parts) != 2:
                raise ValueError(f"Invalid line (expected lon,lat): {ln}")
            pts.append((float(parts[0]), float(parts[1])))
        if len(pts) < 3:
            raise ValueError("Polygon needs at least 3 coordinates.")
        return pts

col1, col2 = st.columns([1,1])
with col1:
    check = st.button("✅ Check")
with col2:
    clear = st.button("🧹 Clear")

if clear:
    st.experimental_rerun()

if check:
    try:
        lon_p, lat_p = parse_point(point_text)
        poly_coords = parse_polygon(poly_text, mode)

        poly = Polygon(poly_coords)
        fix_info = None
        if not poly.is_valid:
            fix_info = explain_validity(poly)
            poly = poly.buffer(0)

        pt = Point(lon_p, lat_p)

        on_boundary = poly.boundary.contains(pt)
        inside = poly.contains(pt)

        if on_boundary:
            verdict = "🟡 On boundary"
        elif inside:
            verdict = "🟢 Inside"
        else:
            verdict = "🔴 Outside"

        st.subheader(f"Result: {verdict}")
        if fix_info:
            st.caption(f"Note: input polygon was invalid and auto-corrected: {fix_info}")

        # Build map
        avg_lat = sum(lat for lon, lat in poly_coords) / len(poly_coords)
        avg_lon = sum(lon for lon, lat in poly_coords) / len(poly_coords)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, control_scale=True)

        folium.Polygon(
            locations=[(lat, lon) for lon, lat in poly_coords],
            color="blue",
            weight=2,
            fill=True,
            fill_opacity=0.35
        ).add_to(m)

        folium.Marker(
            location=(lat_p, lon_p),
            popup=f"Point: {lon_p:.6f}, {lat_p:.6f} → {verdict}",
            tooltip="Test point",
            icon=folium.Icon(color=("green" if inside else ("orange" if on_boundary else "red")))
        ).add_to(m)

        st_folium(m, height=520, width=720)

    except Exception as e:
        st.error(str(e))
