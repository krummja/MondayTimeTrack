from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    pass

from monday_time_track._types import TransformationType, TRANSFORMATION_TYPES


def transform_text_service(value: str, transformation_type: TransformationType):
    match transformation_type['value']:
        case 'TO_UPPER_CASE':
            return value.upper()
        case 'TO_LOWER_CASE':
            return value.lower()
        case _:
            return value.upper()
