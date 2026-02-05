# CountryFinder

A Python package for finding the country of any point on earth offline.

## Installation

```bash
pip install countryfinder
```

## Quick Start

### Functional interface

```python
from countryfinder import country_at, get_geometry

# Find country at coordinates
country = country_at(lng=4.3485, lat=50.8029)
print(country.name)  # Belgium

# Get country geometry
geometry = get_geometry(alpha_3="BEL")
print(geometry)
```

### Object-oriented interface

```python
from countryfinder import CountryFinder

# Create finder instance
finder = CountryFinder()

# Find country at coordinates
country = finder.country_at(lng=4.3485, lat=50.8029)
print(country.name)  # Belgium

# Get country boundary geometry
geometry = finder.get_geometry(alpha_3="BEL")
```

## References

CountryFinder uses the [geoBoundaries](https://www.geoboundaries.org/) Comprehensive Global Administrative Zones (CGAZ) dataset, which provides simplified administrative boundaries for every country in the world. The data is automatically downloaded on first use. For country names, codes, and other metadata [pycountry](https://github.com/pycountry/pycountry) is used, which implements the ISO 3166-1 standard.
