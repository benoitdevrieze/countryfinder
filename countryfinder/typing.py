from typing import Protocol

class Country(Protocol):
    alpha_2: str
    alpha_3: str
    numeric: str
    name: str
    official_name: str
    flag: str
