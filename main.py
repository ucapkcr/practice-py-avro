import avro
import py_avro_schema as pas

from models.from_dataclasses import Ship, Coordinate
from models.from_pydantic import Boat

# Create an avro schema JSON from a dataclass model
avro_json = pas.generate(Ship)
print(avro_json.decode())

# Notice difference in namespace with and without this option
avro_json = pas.generate(Ship, options=pas.Option.AUTO_NAMESPACE_MODULE)
print(avro_json.decode())
# options=pas.Option.NO_AUTO_NAMESPACE would remove namespace altogether

# Testing handling of optional fields
avro_json = pas.generate(Coordinate)
print(avro_json.decode())
# If you want to force all fields to have a default use: py_avro_schema.Option.DEFAULTS_MANDATORY

# You can disable auto-generation of the doc
avro_json = pas.generate(Coordinate, options=pas.Option.NO_DOC)
print(avro_json.decode())

# Create an avro schema JSON from a pydantic 2.0+ model with a field description
avro_json = pas.generate(Boat, options=pas.Option.AUTO_NAMESPACE_MODULE)
print(avro_json.decode())
# This can be disabled with options=py_avro_schema.Option.NO_DOC


