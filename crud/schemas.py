from pydantic import BaseModel

class CRUD(BaseModel):
    title: str
    text: str
    date: str
    author: str