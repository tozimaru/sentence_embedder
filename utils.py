from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    content: str
    title: str
    author: Optional[str] = None
    written_year: Optional[int] = None
    document_type: str

class Query(BaseModel):
    sentences: List[str]
    k: int
    threshold: Optional[float] = None
