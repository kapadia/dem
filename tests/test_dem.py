
import os
import json
from dem import dem


def test_extract_elevation_points():
    
    testdir = os.path.dirname(os.path.realpath(__file__))
    
    srcpath = os.path.join(testdir, 'fixtures', 'buttermilks.geojson')
    dstpath = os.path.join(testdir, 'fixtures', 'dem.tif')
    # with open(srcpath, 'r') as src:
    #     data = json.loads(src.read())
    
    print dem.toDigitalElevationModel(srcpath, dstpath)
    assert False
