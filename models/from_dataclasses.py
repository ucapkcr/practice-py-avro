import dataclasses


@dataclasses.dataclass
class Ship:
    """A beautiful ship"""

    name: str
    year_launched: int

@dataclasses.dataclass
class Coordinate:
    """Testing optional fields"""

    x: str
    y: int | None = None
