import os
from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    'numpy',
    'rasterio',
    'shapely',
    'pyproj',
    ]

setup(
    name='extract',
    version=0.1,
    description="Extracting your polygons from geospatial rasters.",
    license='MIT',
    keywords='gis data computation raster images maps',
    author='Daven Quinn',
    author_email='dev@davenquinn.com',
    maintainer='Daven Quinn',
    maintainer_email='dev@davenquinn.com',
    url='http://github.com/davenquinn/extract',
    install_requires=install_requires,
    tests_require=['nose'],
    test_suite='nose.collector',
    packages=find_packages(),
    package_dir={'imagery':'.'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
