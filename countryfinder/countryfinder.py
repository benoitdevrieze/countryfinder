from typing import overload

from abc import ABC, abstractmethod

import os
import urllib.parse
import requests

import geopandas as gpd

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
        cgaz_shapefile_path = self._download_cgaz_shapefile()
        self._boundaries = gpd.read_file(cgaz_shapefile_path).to_crs('EPSG:4326').set_index('shapeGroup')

    def country_at(self, *, lng: float, lat: float) -> str | None:
        return self.country_by_geometry(Point(lng, lat))
    
    def country_by_geometry(self, geometry: BaseGeometry) -> str | None:
        point = geometry.representative_point() # use representative point for speed
        results = self._boundaries[self._boundaries.geometry.contains(point)]
        return results.index[0] if not results.empty else None

    def get_geometry(self, *, alpha_3: str):
        self._boundaries.geometry.loc[alpha_3]

    def _download_cgaz_shapefile(self) -> str:

        shapefile_url = 'https://github.com/wmgeolab/geoBoundaries/raw/refs/heads/main/releaseData/CGAZ/geoBoundariesCGAZ_ADM0.zip'
        shapefile_path = os.path.join(self._data_root, os.path.basename(urllib.parse.urlparse(shapefile_url).path))

        if not os.path.exists(shapefile_path):

            if not os.path.exists(self._data_root):
                os.makedirs(self._data_root)

            response = requests.get(shapefile_url)
            with open(shapefile_path, "wb") as datafile:
                datafile.write(response.content)
        
        return shapefile_path
