"""
Interpolation strategies for image pixel extraction.

Possible options are:

- `nearest`
- `bilinear`
- `cubic`

"""
from __future__ import division

import numpy as N
import logging as log

from scipy.ndimage import map_coordinates
from shapely.geometry import shape, mapping, asLineString


def __factory__(order):
	log.info("Initializing an interpolation function of order {0}".format(order))

	def interpolate(array,geometry):
		"""Interpolates geometries to the specified order"""
		def point_handler(coords):
			return line_handler([coords])[0]

		def line_handler(coords):
			coordinates = N.array(coords)
			aligned = (coordinates - 0.5)[:,0:2].T[::-1]  # align fractional pixel coordinates to array
			z = map_coordinates(array, aligned, mode="nearest", order=order)
			try:
				coordinates[:,2] = z
			except IndexError:
				coordinates = N.hstack((coordinates,z.reshape(len(z),1)))
			return list(map(tuple, coordinates))

		if geometry.geom_type == "Point":
			geometry.coords  = point_handler(geometry.coords)
		else:
			geometry.coords = line_handler(geometry.coords)
		return geometry
	return interpolate

nearest = __factory__(0)
bilinear = __factory__(1)
cubic = __factory__(2)
