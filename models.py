from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    store_name = Column(String, index=True)
    price = Column(Float)
    rating = Column(Float)
    total_reviews = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    store_name = Column(String, index=True)
    review_text = Column(Text)
    sentiment = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
