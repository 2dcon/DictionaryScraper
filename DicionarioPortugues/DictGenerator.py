from dataclasses import dataclass


@dataclass
class dictEntry:
    key: str
    text: str


@dataclass
class Extracted:
    text: str
    section_length: int
