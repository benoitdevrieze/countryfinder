from typing import overload

from abc import ABC, abstractmethod

import os
import urllib.parse
import requests
import functools

import pycountry

import geopandas as gpd

from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from countryfinder.config import DEFAULT_DATA_ROOT



class CountryFinderABC(ABC):

    @abstractmethod
    def country_at(self, *, lng: float, lat: float) -> str | None: ...

    @abstractmethod
    def get_geometry(self, *, alpha_3: str) -> BaseGeometry | None: ...



class CountryFinder(CountryFinderABC):


    def __init__(self, data_root: str | None = None):
        super().__init__()
        self._data_root = data_root if data_root is not None else DEFAULT_DATA_ROOT
        self._boundaries_by_code: dict[str, GeoDataFrame] = {}
        self._boundaries_by_name: dict[str, GeoDataFrame] = {}


    def country_at(self, *, lng: float, lat: float) -> str | None:
        return self.country_by_geometry(Point(lng, lat))


    def country_by_geometry(self, geometry: BaseGeometry) -> str | None:
        point = geometry.representative_point() # use representative point for speed
        boundaries = self._get_boundaries_by_code(level='ADM0')
        results = boundaries[boundaries.geometry.contains(point)]
        return pycountry.countries.get(alpha_3=results.index[0]).alpha_2 if not results.empty else None


    def get_geometry(self, code: str):
        return self.get_subdivision_geometry(code) or self.get_country_geometry(code)


    def get_subdivision_geometry(self, code: str) -> BaseGeometry | None:
        if subdivision := pycountry.subdivisions.get(code=code):
            level = self._discover_subdivision_level(subdivision)
            boundaries = self._get_boundaries_by_name(f'ADM{level}')
            return boundaries.geometry.loc[subdivision.name]
        return None
        

    def get_country_geometry(self, code: str) -> BaseGeometry | None:
        if country := pycountry.countries.get(alpha_2=code) or pycountry.countries.get(alpha_3=code) or pycountry.countries.get(numeric=code):
            boundaries = self._get_boundaries_by_code(f'ADM0')
            return boundaries.geometry.loc[country.alpha_3]
        return None

    
    def _discover_subdivision_level(self, subdivision, level: int = 1):
        return self._discover_subdivision_level(subdivision.parent, level + 1) if subdivision.parent else level
    

    def _get_boundaries_by_code(self, level: str) -> GeoDataFrame:
        if level not in self._boundaries_by_code:
            self._load_boundaries(level)
        return self._boundaries_by_code[level]
    

    def _get_boundaries_by_name(self, level: str) -> GeoDataFrame:
        if level not in self._boundaries_by_name:
            self._load_boundaries(level)
        return self._boundaries_by_name[level]


    def _load_boundaries(self, level: str) -> GeoDataFrame:
        shapefile_url = f'https://github.com/wmgeolab/geoBoundaries/raw/refs/heads/main/releaseData/CGAZ/geoBoundariesCGAZ_{level.upper()}.zip'
        shapefile_path = os.path.join(self._data_root, os.path.basename(urllib.parse.urlparse(shapefile_url).path))

        if not os.path.exists(shapefile_path):

            if not os.path.exists(self._data_root):
                os.makedirs(self._data_root)

            response = requests.get(shapefile_url)
            with open(shapefile_path, "wb") as datafile:
                datafile.write(response.content)
        
        boundaries = gpd.read_file(shapefile_path).to_crs('EPSG:4326')

        boundaries = boundaries[boundaries['shapeType'] == level]

        self._boundaries_by_code[level] = boundaries.set_index('shapeGroup')
        self._boundaries_by_name[level] = boundaries.set_index('shapeName')
