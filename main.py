from motor.motor_asyncio import AsyncIOMotorDatabase

from models import Product, Review
import datetime
from fastapi import FastAPI, Request, HTTPException
from database import products_collection, reviews_collection, markets_collection
# from sentiment_model import analyze_sentiment
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# اضافه کردن پوشه استاتیک برای لود فایل‌های CSS، JS و تصاویر
app.mount("/static", StaticFiles(directory="static"), name="static")

# تنظیم مسیر قالب‌های HTML
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/monitoring")
async def monitoring_root(request: Request):
    return templates.TemplateResponse("monitoring.html", {"request": request})


@app.get("/resources")
async def read_root(request: Request):
    return templates.TemplateResponse("resources.html", {"request": request})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # اجازه دسترسی به همه منابع
    allow_credentials=True,
    allow_methods=["*"],  # اجازه استفاده از همه متدها
    allow_headers=["*"],  # اجازه استفاده از همه هدرها
)


class ProductSchema(BaseModel):
    product_real_id: str
    name: str
    category: str
    store_name: str
    price: float
    rating: float
    total_reviews: int
    market_id: int


class ReviewSchema(BaseModel):
    product_id: str
    store_name: str
    review_text: str
    market_id: int


class MarketCreate(BaseModel):
    name: str
    market_id: int


# 📌 افزودن یک مارکت جدید با دریافت ورودی
@app.post("/add-market/")
async def add_market(market: MarketCreate):
    await markets_collection.insert_one(market.dict())
    return {"message": f"✅ مارکت '{market.name}' با موفقیت اضافه شد."}


# 📌 دریافت لیست تمامی مارکت‌ها
@app.get("/markets/")
async def get_markets():
    markets = await markets_collection.find().to_list(length=None)
    for market in markets:
        market["_id"] = str(market["_id"])
    return {"markets": markets}


# 📌 حذف یک مارکت بر اساس ID
@app.delete("/markets/{market_id}")
async def delete_market(market_id: int):
    result = await markets_collection.delete_one({"market_id": market_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="مارکت یافت نشد")
    return {"message": "مارکت حذف شد"}


@app.post("/add_product/")
async def add_product(product: ProductSchema):
    print(product)
    print('[[[[[[[[[[[[[[[[[product]]]]]]]]]]]]]]]]]')
    new_product = await products_collection.insert_one(product.dict())
    return {"id": str(new_product.inserted_id)}


@app.post("/add_review/")
async def add_review(review: ReviewSchema):
    # sentiment = await analyze_sentiment(review.review_text)
    new_review = {
        "product_id": review.product_id,
        "store_name": review.store_name,
        "review_text": review.review_text,
        "sentiment": "sentiment",
        "created_at": datetime.datetime.utcnow()
    }
    await reviews_collection.insert_one(new_review)
    return {"message": "Review added successfully", "sentiment": "sentiment"}


@app.get("/search/")
async def search_products(query: str):
    cursor = products_collection.find({"name": {"$regex": query, "$options": "i"}}).limit(10)
    products = await cursor.to_list(length=10)
    print([{"id": str(p["_id"]), "name": p["name"], "store": p["store_name"]} for p in products])
    return [{"id": str(p["_id"]), "name": p["name"], "store": p["store_name"]} for p in products]


@app.get("/product_reviews/{product_id}/{store_name}/")
async def get_product_reviews(product_id: str, store_name: str):
    cursor = reviews_collection.find({"product_id": product_id, "store_name": store_name})
    reviews = await cursor.to_list(length=100)
    return [{"text": r["review_text"], "sentiment": r["sentiment"]} for r in reviews]


@app.get("/sentiment_chart/{product_id}/{store_name}/")
async def sentiment_chart(product_id: str, store_name: str):
    cursor = reviews_collection.find({"product_id": product_id, "store_name": store_name})
    reviews = await cursor.to_list(length=100)

    sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}
    for review in reviews:
        sentiment_count[review["sentiment"]] += 1

    return sentiment_count

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
