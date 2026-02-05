from typing import overload

from abc import ABC, abstractmethod

import os
import urllib.parse
import requests

import geopandas as gpd

from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from countryfinder.config import DEFAULT_DATA_DIR



class AbstractCountryFinder(ABC):

    def __init__(self, data_path: str | None = None):
        super().__init__()
        self._data_path = data_path if data_path is not None else DEFAULT_DATA_DIR

    @abstractmethod
    def country_at(self, *, lng: float, lat: float) -> str | None: ...

    @overload
    def get_geometry(self, *, alpha_2: str) -> BaseGeometry | None: ...

    @overload
    def get_geometry(self, *, alpha_3: str) -> BaseGeometry | None: ...

    @overload
    def get_geometry(self, *, numeric: str) -> BaseGeometry | None: ...

    @overload
    def get_geometry(self, *, name: str) -> BaseGeometry | None: ...

    @abstractmethod
    def get_geometry(self, **kwargs): ...


class CountryFinder(AbstractCountryFinder):

    def __init__(self, data_path: str | None = None):
        super().__init__(data_path)
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
        shapefile_path = os.path.join(self._data_path, os.path.basename(urllib.parse.urlparse(shapefile_url).path))

        if not os.path.exists(shapefile_path):

            response = requests.get(shapefile_url)
            with open(shapefile_path, "wb") as datafile:
                datafile.write(response.content)
        
        return shapefile_path
