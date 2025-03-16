from pydantic import BaseModel

class ProductSchema(BaseModel):
    name: str
    category: str
    store_name: str
    price: float
    rating: float
    total_reviews: int

class ReviewSchema(BaseModel):
    product_id: int
    store_name: str
    review_text: str
