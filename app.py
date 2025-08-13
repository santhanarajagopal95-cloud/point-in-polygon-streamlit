!pip install shapely ipywidgets

from shapely.geometry import Point, Polygon
import ipywidgets as widgets
from IPython.display import display, HTML

# Text boxes for input
polygon_input = widgets.Textarea(
    value="79.3479688288648,10.98775809708549\n79.32348738181935,11.005293262398226\n79.30032934779183,10.980610758801461\n79.30760632236604,10.913055003692932\n79.3532614415277,10.870823079150227\n79.41611903303561,10.880568878683093\n79.4346410300393,10.954630465654162\n79.4187629197537,10.987757360769919\n79.3479688288648,10.98775809708549",
    description="Polygon (lon,lat per line):",
    layout=widgets.Layout(width="600px", height="200px")
)

point_input = widgets.Text(
    value="79.23483023084555,11.015679746362835",
    description="Point (lon,lat):",
    layout=widgets.Layout(width="600px")
)

# Output area
output = widgets.Output()

# Function to check point inside polygon
def check_point(_):
    output.clear_output()
    try:
        # Parse polygon
        poly_coords = []
        for line in polygon_input.value.strip().split("\n"):
            lon, lat = map(float, line.strip().split(","))
            poly_coords.append((lon, lat))
        
        # Parse point
        lon_p, lat_p = map(float, point_input.value.strip().split(","))
        
        polygon = Polygon(poly_coords)
        point = Point(lon_p, lat_p)
        
        result = "✅ Inside" if polygon.contains(point) else "❌ Outside"
        
        with output:
            display(HTML(f"<h3>Result: {result}</h3>"))
    except Exception as e:
        with output:
            display(HTML(f"<p style='color:red;'>Error: {e}</p>"))

# Button
check_button = widgets.Button(description="Check", button_style='success')
check_button.on_click(check_point)

# Show UI
display(polygon_input, point_input, check_button, output)
