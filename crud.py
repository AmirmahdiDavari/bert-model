from sqlalchemy.orm import Session
from models import Product, Review
from sentiment_model import analyze_sentiment
from schemas import ReviewSchema


def get_top_products(db: Session, query: str):
    return db.query(Product).filter(Product.name.ilike(f"%{query}%")).limit(10).all()


def add_review(db: Session, review: ReviewSchema):
    sentiment = analyze_sentiment(review.review_text)
    new_review = Review(
        product_id=review.product_id,
        store_name=review.store_name,
        review_text=review.review_text,
        sentiment=sentiment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_reviews_by_product(db: Session, product_id: int, store_name: str):
    return db.query(Review).filter(Review.product_id == product_id, Review.store_name == store_name).all()


def get_sentiment_summary(db: Session, product_id: int, store_name: str):
    reviews = db.query(Review).filter(Review.product_id == product_id, Review.store_name == store_name).all()
    sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}
    for review in reviews:
        sentiment_count[review.sentiment] += 1
    return sentiment_count
