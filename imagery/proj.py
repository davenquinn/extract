import fiona
from pyproj import Proj, transform
from shapely.geometry import mapping, shape
import logging as log
from functools import partial

def transform_coords(func, records):
    """
    Transform record geometry coordinates using the provided function.
    .. http://sgillies.net/blog/1125/fiona-pyproj-shapely-in-a-functional-style/
    """
    for rec in records:
        if rec['geometry']['type'] == "LineString":
        	coords = func(*zip(*rec["geometry"]["coordinates"]))
        	coords = zip(*coords)
        if rec['geometry']['type'] == "Point":
        	coords = func(*rec["geometry"]["coordinates"])
        rec['geometry']['coordinates'] = coords
        yield rec

def setup_proj(prj):
	try:
		return Proj(prj)
	except RuntimeError:
		return Proj({"proj":"latlong"})

class Transformation(object):
    def __init__(self, source, sink):
    	self.source = setup_proj(source)
        self.sink = setup_proj(sink)

    def transform(self, records):
        func = partial(transform, self.source, self.sink)
        return transform_coords(func, records)

    def reversed(self, records):
        func = partial(transform, self.sink, self.source)
        return transform_coords(func, records)

