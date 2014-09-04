"""
Several methods for computing windowed spectra of a CRISM image given a series of numerical masks.
"""
import rasterio
import numpy as N
from osgeo import gdal as G

def create_mask(dataset, geometry):
    """ Returns a boolean array that is `true` where a geometry exists
        and `false` otherwise."""
    height, width = dataset.shape
    pixels = polygon.exterior.coords
    # PIL regrettably works in the reverse coordinate order
    # But shapely shapes (and other geo-things) are already x-first
    img = Image.new('L', (width, height), 0)
    ImageDraw.Draw(img).polygon(pixels, outline=1, fill=1)
    arr =  N.array(img, dtype=bool)
    assert arr.shape == shape
    return arr

def offset_mask(mask):
    """ Returns a mask shrunk to the 'minimum bounding rectangle' of the
        nonzero portion of the previous mask, and its offset from the original.
        Useful to find the smallest rectangular section of the image that can be
        extracted to include the entire geometry. Conforms to the y-first
        expectations of numpy arrays rather than x-first (geodata).
    """
    def axis_data(axis):
        """Gets the bounds of a masked area along a certain axis"""
        x = mask.sum(axis)
        trimmed_front = N.trim_zeros(x,"f")
        offset = len(x)-len(trimmed_front)
        size = len(N.trim_zeros(trimmed_front,"b"))
        return offset,size

    xo,xs = axis_data(0)
    yo,ys = axis_data(1)

    array = mask[yo:yo+ys,xo:xo+xs]
    offset = (yo,xo)
    return array, offset

def mask_shape(mask,axis=0):
    x = mask.sum(axis)
    xi = N.trim_zeros(x,"f")
    xo = len(x)-len(xi)
    xs = len(N.trim_zeros(xi,"b"))
    return xo,xs

def extract_area(dataset, geometry, **kwargs):
    """
    Compute a spectrum using the basic GDAL driver to read a single band of the spectrum.
    This is faster than the rasterio version and is the default.
    """
    im = dataset.__gdal__
    bands = kwargs.pop("bands", list(range(im.RasterCount)))

    mask = create_mask(dataset,geometry)
    maskt, offset = offset_mask(mask)
    yo,xo = offset
    ys,xs = maskt.shape
    for i in (0,1):
        assert N.allclose(maskt.sum(axis=i), N.trim_zeros(mask.sum(axis=i)))

    maskt = maskt.transpose() # Conform to GDAL's fascist X-first expectations
    maska = N.repeat(
        N.expand_dims(maskt,0),
        len(bands),
        axis=0)
    buffer=im.ReadRaster(xo,yo,xs,ys,
        band_list=[b+1 for b in bands])
    arr = N.fromstring(buffer, dtype=dataset.dtype)
    arr = arr.reshape((len(bands), xs, ys))
    arr = N.ma.masked_array(arr, arr==dataset.nodata)
    arr[maska==False] = N.ma.masked
    xarr = N.array([xo+0.5 for i in range(xs)]).reshape((xs,0))
    yarr = N.array([yo+0.5 for i in range(ys)]).reshape((ys,1))

    import IPython; IPython.embed()
    return arr

def iterated(image, masks, verbose=True):
    """
    This method uses `rasterio` to read the bands and apply the mask in sequence.
    It is slower and suffers from memory-use issues but is much terser and easier
    to understand. It is used primarily as a test case for the faster method.
    """
    def average(band, mask):
        a = band[mask==True]
        val = a.mean()
        a = None
        return val

    def main():
        with rasterio.drivers():
            with rasterio.open(image.trdr,"r") as src:
                for i,nan in zip(src.indexes, src.nodatavals):
                    band = src.read_band(i)
                    if verbose: print(i)
                    yield tuple(average(band, mask) for mask in masks)
                    band = None

    return zip(*tuple(main()))

def compute_spectrum(image, masks, **kwargs):
    """
    Computes the spectrum of the image for a series of masks.
    kwargs:
        method="chunk" (can also set to "iterate")
        verbose=False
    """
    method = kwargs.pop("method", "chunk")
    methods = dict(
        chunk=chunked,
        iterate=iterated)
    return methods[method](image, masks, **kwargs)
