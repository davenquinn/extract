`extract` is a python module that builds off of `rasterio` functionality
to allow the extraction of image pixels in areas corresponding to
polygon geometries.

## Usage

Input takes shapely geometries and (optional) crs mapping for shape
spatial reference.

```python
>>> syrtis_tm = {
    'a': 3396190,
    'b': 3376200,
    'k': 0.9996,
    'lat_0': 17,
    'lon_0': 76.5,
    'no_defs': True,
    'proj': u'tmerc',
    'units': u'm',
    'x_0': 0,
    'y_0': 0}

>>> repr(landing_ellipse)
<shapely.geometry.polygon.Polygon at 0x10fc6c810>
```

Then you can extract the shape from a `rasterio` dataset.

```python
>>> import rasterio
>>> from extract import extract_area

>>> with rasterio.open(hrsc_mosaic) as dem:
        array = extract_area(dem,
            to_shape(landing_ellipse),
            feature_crs=syrtis_tm)

>>> array.min(), array.max()
(-2441, -2094)
```

The output array is 3-dimensional `numpy` `MaskedArray` (masked by the shape boundaries)
with a first dimension corresponding to the number of bands extracted.

```python
>>> array.shape
(1, 281, 332)
```

It also has an attached `offset` property that contains its (y,x)-indexed distance
from the image origin.

```python
>>> array.offset
(17949, 3484)
```

## Installation

For now, this can be installed as a standalone module:

```
~ pip install git+https://github.com/davenquinn/extract.git
```

I'd like to see this functionality integrated into `rasterio` itself;
stay tuned!

