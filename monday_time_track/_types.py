from typing import TypedDict, List


class TransformationType(TypedDict):
    title: str
    value: str


TRANSFORMATION_TYPES: List[TransformationType] = [
    {'title': 'to upper case', 'value': 'TO_UPPER_CASE'},
    {'title': 'to lower case', 'value': 'TO_LOWER_CASE'},   
]
