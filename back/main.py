from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List
from crawler import converter, categories, subcategories
from urllib.parse import unquote, quote

# Create FastAPI app
app = FastAPI()

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Item model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    subcategory = Column(String, index=True)
    original_title = Column(String, index=True)
    new_title = Column(String)
    summary = Column(String)
    news_link = Column(String)
    news_body = Column(String)

# Pydantic model for Item creation
class ItemCreate(BaseModel):
    category_choice: int
    subcategory_choice: int

# Pydantic model for Item response
class ItemResponse(BaseModel):
    id: int
    category: str
    subcategory: str
    original_title: str
    new_title: str
    summary: str
    news_link: str
    news_body: str

    class Config:
        orm_mode = True

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Reflect the tables
metadata = MetaData()
metadata.reflect(bind=engine)

# Drop the existing table if it exists
if 'items' in metadata.tables:
    Item.__table__.drop(engine)

# Recreate the table with the correct schema
Base.metadata.create_all(bind=engine)

# Define your FastAPI endpoints
@app.post("/items/", response_model=List[ItemResponse])
def create_items(item: ItemCreate, db: Session = Depends(get_db)):
    category_name, subcategory_name = categories[item.category_choice][0], subcategories[categories[item.category_choice][0]][item.subcategory_choice][0]
    converted_data = converter(item.category_choice, item.subcategory_choice)
    
    if not converted_data:
        raise HTTPException(status_code=404, detail="No news articles found")

    stored_items = []
    for data in converted_data:
        db_item = Item(
            category=category_name,
            subcategory=subcategory_name,
            original_title=data['original_title'],
            new_title=data['generated_title'],
            summary=data['summary'],
            news_link=data['link'],
            news_body=data['content']
        )
        db.add(db_item)
        stored_items.append(db_item)
    
    db.commit()
    for item in stored_items:
        db.refresh(item)

    return stored_items

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items/", response_model=List[ItemResponse])
def read_all_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items

@app.get("/items/category/", response_model=List[ItemResponse])
def read_items_by_category(category: str = Query(...), db: Session = Depends(get_db)):
    decoded_category = unquote(category)
    items = db.query(Item).filter(Item.category == decoded_category).all()
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")
    return items

@app.get("/items/category/subcategory/", response_model=List[ItemResponse])
def read_items_by_category_and_subcategory(category: str = Query(...), subcategory: str = Query(...), db: Session = Depends(get_db)):
    decoded_category = unquote(category)
    decoded_subcategory = unquote(subcategory)
    
    # Debugging output
    print(f"Decoded Category: {decoded_category}")
    print(f"Decoded Subcategory: {decoded_subcategory}")
    
    items = db.query(Item).filter(Item.category == decoded_category, Item.subcategory == decoded_subcategory).all()
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")
    return items