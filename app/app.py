from flask import Flask, render_template
import os
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import folium

# Initialize Flask app
app = Flask(__name__)

# Define paths
NDVI_PATH = os.path.join('data', 'processed', 'NDVI_Punjab_2023.tif')
YIELD_DATA = {
    'Zone 1': 80,
    'Zone 2': 60,
    'Zone 3': 90,
}

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to display NDVI map
@app.route('/ndvi_map')
def ndvi_map():
    # Create a Folium map
    m = folium.Map(location=[30.9, 75.8], zoom_start=10)

    # Add NDVI layer to the map
    folium.raster_layers.ImageOverlay(
        image=NDVI_PATH,
        bounds=[[29.5, 74.5], [31.5, 76.5]],  # ROI bounds
        colormap=lambda x: (1, 0, 0, x)  # Red colormap
    ).add_to(m)

    # Save the map to an HTML file
    map_path = os.path.join('app', 'templates', 'ndvi_map.html')
    m.save(map_path)

    return render_template('ndvi_map.html')

# Route to display NDVI plot
@app.route('/ndvi_plot')
def ndvi_plot():
    # Load NDVI data
    with rasterio.open(NDVI_PATH) as src:
        ndvi = src.read(1)

    # Plot NDVI
    plt.figure(figsize=(10, 10))
    show(ndvi, cmap='YlGn', title='NDVI')
    plt.colorbar(label='NDVI')
    plot_path = os.path.join('app', 'static', 'ndvi_plot.png')
    plt.savefig(plot_path)
    plt.close()

    return render_template('ndvi_plot.html', plot_path=plot_path)

# Route to display yield prediction
@app.route('/yield_prediction')
def yield_prediction():
    return render_template('yield_prediction.html', yield_data=YIELD_DATA)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)