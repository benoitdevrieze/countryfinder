from typing import overload

from shapely.geometry.base import BaseGeometry

from countryfinder.countryfinder import CountryFinder


CF_INSTANCE: CountryFinder = None    # singleton


def _get_cf_instance() -> CountryFinder:

    global CF_INSTANCE
    
    if CF_INSTANCE is None:
        CF_INSTANCE = CountryFinder()
    
    return CF_INSTANCE


def country_at(*, lng: float, lat: float) -> str | None:
    return _get_cf_instance().country_at(lng=lng, lat=lat)


def country_by_geometry(geometry: BaseGeometry) -> str | None:
    return _get_cf_instance().country_by_geometry(geometry)


def get_geometry(code: str) -> BaseGeometry | None:
    return _get_cf_instance().get_geometry(code)


def get_subdivision_geometry(code: str) -> BaseGeometry | None:
    return _get_cf_instance().get_subdivision_geometry(code)


def get_country_geometry(code: str) -> BaseGeometry | None:
    return _get_cf_instance().get_country_geometry(code)
