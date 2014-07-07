import os
from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    'numpy',
    'scipy',
    'matplotlib',
    'fiona',
    'shapely',
    'pyproj',
    'gdal'
    ]

setup(
    name='Imagery',
    version=0.1,
    description="Imagery is a thin wrapper to the Python GDAL bindings.",
    license='MIT',
    keywords='gis data computation raster images maps',
    author='Daven Quinn',
    author_email='dev@davenquinn.com',
    maintainer='Daven Quinn',
    maintainer_email='dev@davenquinn.com',
    url='http://github.com/davenquinn/Imagery',
    install_requires=install_requires,
    tests_require=['nose'],
    test_suite='nose.collector',
    packages=find_packages(),
    package_dir={'imagery':'imagery'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
