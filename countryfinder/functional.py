from typing import overload

from shapely.geometry.base import BaseGeometry

from countryfinder.countryfinder import CountryFinder
from countryfinder.typing import Country


CF_INSTANCE: CountryFinder = None    # singleton


def _get_cf_instance() -> CountryFinder:

    global CF_INSTANCE
    
    if CF_INSTANCE is None:
        CF_INSTANCE = CountryFinder()
    
    return CF_INSTANCE


def country_at(*, lng: float, lat: float) -> Country | None:
    return _get_cf_instance().country_at(lng=lng, lat=lat)


def country_by_geometry(geometry: BaseGeometry) -> Country | None:
    return _get_cf_instance().country_by_geometry(geometry)


@overload
def get_geometry(*, alpha_2: str) -> BaseGeometry | None: ...

@overload
def get_geometry(*, alpha_3: str) -> BaseGeometry | None: ...

@overload
def get_geometry(*, numeric: str | int) -> BaseGeometry | None: ...

@overload
def get_geometry(*, name: str) -> BaseGeometry | None: ...

def get_geometry(**kwargs):
    return _get_cf_instance().get_geometry(**kwargs)
