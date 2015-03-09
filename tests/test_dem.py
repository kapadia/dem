
import os
import json
from dem import dem


def test_extract_elevation_points():
    
    testdir = os.path.dirname(os.path.realpath(__file__))
    
    srcpath = os.path.join(testdir, 'fixtures', 'druids.geojson')
    dstpath = os.path.join(testdir, 'fixtures', 'dem.tif')
    
    print dem.toDigitalElevationModel(srcpath, dstpath)
    assert False
