
# Point in Polygon Checker (Streamlit)

A tiny web app to test whether a point (lon,lat) lies Inside / Outside a polygon.  
Supports lon,lat-per-line input or GeoJSON Polygon. Renders an interactive map.

## Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Push this folder to a **public GitHub repo**.
2. Go to https://streamlit.io/cloud → **Deploy an app**.
3. Select your repo/branch and set the main file to `app.py`.
4. You’ll get a public URL when the build finishes.

## Deploy to Hugging Face Spaces
1. Create a new **Space** using the **Streamlit** SDK.
2. Upload `app.py` and `requirements.txt`.
3. Commit → App goes live with a public link.
