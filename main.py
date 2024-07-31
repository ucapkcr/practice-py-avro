import io

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import BinaryDecoder, BinaryEncoder, DatumReader, DatumWriter 
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

# Now to actually write some avro binary...
schema = avro.schema.parse(open("example.avro.User.avsc", "rb").read())

writer = DataFileWriter(open("users.avro", "wb"), DatumWriter(), schema)
writer.append({"name": "Alyssa", "favorite_number": 256})
writer.append({"name": "Ben", "favorite_number": 7, "favorite_color": "red"})
writer.close()

reader = DataFileReader(open("users.avro", "rb"), DatumReader())
for user in reader:
    print(user)
reader.close()

# What if I want to do IO not write / read from file (e.g. for Kafka)?
writer = DatumWriter(schema)
bytes_writer = io.BytesIO()
encoder = BinaryEncoder(bytes_writer)

payload = {"name": "Chris", "favorite_color": "green", "favorite_number": 7}

writer.write(payload, encoder)
raw_bytes = bytes_writer.getvalue()
print(raw_bytes)

# Then to reverse the process:
bytes_reader = io.BytesIO(raw_bytes)
decoder = BinaryDecoder(bytes_reader)
reader = DatumReader(schema)
recovered_payload = reader.read(decoder)

print(recovered_payload)
print(payload == recovered_payload)

# But what about if I want to use a schema that includes a custom record type in a field? i.e. 2+ schemas needed...
# child_schema = avro.schema.parse(open("example.avro.Favorites.avsc", "rb").read())
# parent_schema = avro.schema.parse(open("example.avro.ComplexUser.avsc", "rb").read())
# Can't seem to get this to work...
