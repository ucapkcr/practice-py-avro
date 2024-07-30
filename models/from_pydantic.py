import pydantic


class Boat(pydantic.BaseModel):
    """A beautiful boat"""

    name: str
    year_launched: int | None = pydantic.Field(None, description="When we hit the water")
