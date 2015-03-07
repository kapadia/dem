
import json
import numpy as np
import rasterio as rio
import pyproj
from affine import Affine

from scipy.interpolate import griddata



def get_elevation(data):
    """
    :param data:
        Parsed GeoJSON data structure.
    """
    coordinates = map(lambda f: f['geometry']['coordinates'], data['features'])
    return [c for clist in coordinates for c in clist]


def get_dimensions(ulx, uly, lrx, lry, resolution=1):
    """
    :param ulx:
    :param uly:
    :param lrx:
    :param lry:
    :param resolution:
        Spatial resolution (meters/pixel) of the output image.
    """
    
    # Determine the number of meters in the image
    src_proj = pyproj.Proj(init='epsg:4326')
    dst_proj = pyproj.Proj(init='epsg:3857')
    
    s0, t0 = pyproj.transform(src_proj, dst_proj, ulx, uly)
    s1, t1 = pyproj.transform(src_proj, dst_proj, lrx, lry)
    
    x1, y1 = pyproj.transform(dst_proj, src_proj, s0 + 1, t0 + 1)
    srx = abs(ulx - x1)
    sry = abs(uly - y1)
    sr = 0.5 * (srx + sry)
    
    ds = round(abs(s1 - s0)) / resolution
    dt = round(abs(t1 - t0)) / resolution
    
    return ds, dt, sr


def get_affine_transform(ulx, uly, lrx, lry, resolution=1):
    """
    :param ulx:
    :param uly:
    :param lrx:
    :param lry:
    :param resolution:
        Spatial resolution in units of the output image.
    """
    geotransform = (ulx, resolution, 0.0, uly, 0.0, -resolution)
    return Affine.from_gdal(*geotransform)


def toDigitalElevationModel(srcpath, dstpath):
    """
    :param srcpath:
        File path to a GeoJSON file. The file must contain
        longitude/latitude and elevation data.
        
    :param dstpath:
        Output file that will contain the DEM.
    """
    
    with open(srcpath, 'r') as src:
        data = json.loads(src.read())
    
    elevation = get_elevation(data)
    longitudes = map(lambda c: c[0], elevation)
    latitudes = map(lambda c: c[1], elevation)
    
    # TODO: Generalize for southern hemisphere
    ulx = min(longitudes)
    uly = max(latitudes)
    lrx = max(longitudes)
    lry = min(latitudes)
    
    width, height, spatial_resolution = get_dimensions(ulx, uly, lrx, lry)
    affine = get_affine_transform(ulx, uly, lrx, lry, resolution=spatial_resolution)
    
    metadata = {
        'driver': 'GTiff',
        'width': width,
        'height': height,
        'dtype': rio.uint16,
        'count': 1,
        'nodata': 0,
        'crs': 'EPSG:4326',
        'transform': affine
    }
    
    with rio.open(dstpath, 'w', **metadata) as dst:
        
        points = np.array([ dst.index(lng, lat) for lng, lat, ele in elevation ])
        values = np.array([ ele for lng, lat, ele in elevation ])
        
        grid_x, grid_y = np.mgrid[0:height, 0:width]
        band = griddata(points, values, (grid_x, grid_y), method='cubic')
        
        dst.write_band(1, np.round(band).astype(np.uint16))
    
    