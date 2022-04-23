from fastapi import FastAPI, Depends, HTTPException, status
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
async def home(db:Session=Depends(get_db)):
    all_data = db.query(models.CRUD).all()
    return all_data

@app.post("/new/")
async def new_data(request: schemas.CRUD, db:Session=Depends(get_db)):
    new = models.CRUD(title=request.title, text=request.text, date=request.date, author=request.author)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@app.get("/{id}/")
async def data_with_id(id,db:Session=Depends(get_db)):
    data = db.query(models.CRUD).filter(models.CRUD.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data is not found")
    return data

@app.put("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_data(id, request: schemas.CRUD, db:Session=Depends(get_db)):
    data = db.query(models.CRUD).filter(models.CRUD.id == id)
    data.update(request)
    db.commit()
    return "Data successfully updated"

@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id, db:Session=Depends(get_db)):
    data = db.query(models.CRUD).filter(models.CRUD.id == id).delete(synchronize_session=False)
    db.commit()
    return "Data deleted!"