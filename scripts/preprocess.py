import ee
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

def mask_clouds(image):
    qa = image.select('QA60')
    cloud_mask = qa.bitwiseAnd(1 << 10).eq(0)
    return image.updateMask(cloud_mask)

def calculate_ndvi(image):
    nir = image.select('B8')
    red = image.select('B4')
    ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
    return image.addBands(ndvi)

def export_ndvi(roi, start_date, end_date, description):
    collection = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    
    collection = collection.map(mask_clouds)
    ndvi_collection = collection.map(calculate_ndvi)
    
    task = ee.batch.Export.image.toDrive(
        image=ndvi_collection.median(),
        description=description,
        scale=10,
        region=roi,
        fileFormat='GeoTIFF',
        maxPixels=1e13
    )
    task.start()
    return task