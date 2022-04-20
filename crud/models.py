from .database import BASE
from sqlalchemy import String, Integer, Column

class CRUD(BASE):
    __tablename__ = 'crud table'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    date = Column(String)
    author = Column(String)
