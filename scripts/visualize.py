import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import folium

def plot_ndvi(ndvi_path):
    with rasterio.open(ndvi_path) as src:
        ndvi = src.read(1)
    
    plt.figure(figsize=(10, 10))
    show(ndvi, cmap='YlGn', title='NDVI')
    plt.colorbar(label='NDVI')
    plt.show()

def create_interactive_map(ndvi_path, bounds):
    m = folium.Map(location=[30.9, 75.8], zoom_start=10)
    folium.raster_layers.ImageOverlay(
        image=ndvi_path,
        bounds=bounds,
        colormap=lambda x: (1, 0, 0, x)
    ).add_to(m)
    return m