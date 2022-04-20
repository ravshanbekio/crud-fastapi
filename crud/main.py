from fastapi import FastAPI, Depends
from .schemas import CRUD
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.BASE.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    return "Hello World"

@app.post("/new/")
async def new_data(request: schemas.CRUD, db:Session=Depends(get_db)):
    new = models.CRUD(title=request.title, text=request.text, date=request.date, author=request.author)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new