from typing import List, Dict
from pydantic import BaseModel


class SelectResponse(BaseModel):
    columns: List[Dict]
    data: List[Dict]
