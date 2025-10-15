# models/subject_model.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict
import random

def gen_subject_id() -> str:
    return f"{random.randint(1, 999):03d}"

def grade_from_mark(mark: int) -> str:
    if mark >= 85: return "HD"
    if mark >= 75: return "D"
    if mark >= 65: return "C"
    if mark >= 50: return "P"
    return "Z"

@dataclass
class Subject:
    id: str
    title: str
    mark: int
    grade: str

    def to_dict(self) -> Dict: return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "Subject":
        return Subject(
            id=str(data.get("id","")),
            title=str(data.get("title","")),
            mark=int(data.get("mark",0)),
            grade=str(data.get("grade",""))
        )
