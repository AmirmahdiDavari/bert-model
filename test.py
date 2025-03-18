import csv
import asyncio
import datetime
import httpx
from motor.motor_asyncio import AsyncIOMotorClient

BASE_URL = "http://127.0.0.1:8000"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "sentiment_analysis_db"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
products_collection = db["products"]
reviews_collection = db["reviews"]




async def import_products_from_csv(file_path):
    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        tasks = []

        for row in reader:
            print(row)
            product = {
                "product_real_id": row["\ufeffid"],
                "name": row["title_fa"],
                "category": f"{row['Category1']} > {row['Category2']}",
                "store_name": row["Seller"],
                "price": float(row["Price"]),
                "rating": float(row["Rate"]),
                "total_reviews": int(row["Rate_cnt"])
            }
            await products_collection.insert_one(product)

            print(product)
            print('[[[[[[[[[[[[[[[[[[[[[[[[product]]]]]]]]]]]]]]]]]]]]]]]]')

    print("Products imported successfully!")


async def import_reviews_from_csv(file_path):
    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        tasks = []
        for row in reader:
            review = {
                "product_id": row["product_id"],
                "store_name": row["seller_title"],
                "review_text": row["body"],
                "sentiment": "sentiment",
                "created_at": datetime.datetime.utcnow()
            }

            await reviews_collection.insert_one(review)
            print(review)
            print('[[[[[[[[[[[[[[review]]]]]]]]]]]]]]')
            # tasks.append(add_review(review))

    print("Reviews imported successfully!")
#

async def main():
    await import_products_from_csv("C:\\Users\\ASUS\\Desktop\\digikala-products.csv")
    # await import_reviews_from_csv("C:\\Users\\ASUS\\Desktop\\digikala-comments.csv")


if __name__ == "__main__":
    asyncio.run(main())
