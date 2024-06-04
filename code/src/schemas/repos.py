from typing import Optional, List
from pydantic import BaseModel

class FileSchema(BaseModel):
    path: str
    key_in_R2: str

class RepoSchema(BaseModel):
    name: str
    owner: str
    stars: Optional[int]
    html_url: Optional[str]
    files: List[FileSchema] = []
