# import asyncio
# import httpx
# import random
# from motor.motor_asyncio import AsyncIOMotorClient
# from config import MONGO_URI
#
# # لیست چند User-Agent برای جلوگیری از بلاک شدن
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# ]
#
# # اتصال به دیتابیس MongoDB
# client = AsyncIOMotorClient(MONGO_URI)
# db = client["sentiment_analysis_db"]
# products_collection = db["products"]
#
#
# async def update_digikala_product(product_id):
#     url = f"https://api.digikala.com/v2/product/{product_id}/"
#
#     headers = {
#         'accept': 'application/json, text/plain, */*',
#         'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
#         'origin': 'https://www.digikala.com',
#         'referer': 'https://www.digikala.com/',
#         'user-agent': random.choice(USER_AGENTS),  # انتخاب یک User-Agent تصادفی
#         'x-web-client': 'desktop',
#         'x-web-optimize-response': '1'
#     }
#
#     try:
#         async with httpx.AsyncClient(timeout=10) as client:  # Timeout اضافه شد
#             response = await client.get(url, headers=headers)
#
#         if response.status_code == 200:
#             json_data = response.json()
#             if json_data.get("status") == 200:
#                 main_webp_url = json_data["data"]["product"]["images"]["main"]["webp_url"][0]
#                 return main_webp_url
#
#     except httpx.ConnectError:
#         print(f"❌ Connection error while fetching product {product_id}")
#     except httpx.HTTPStatusError as e:
#         print(f"⚠️ HTTP error {e.response.status_code} for product {product_id}")
#     except Exception as e:
#         print(f"🚨 Unexpected error: {e}")
#     return None
#
#
# async def update_products():
#     async for product in products_collection.find():
#         product_id = product.get("product_real_id")
#         if product_id:
#             image_url = await update_digikala_product(product_id)
#             if image_url:
#                 await products_collection.update_one({"_id": product["_id"]}, {"$set": {"image": image_url}})
#                 print(f"✅ Updated product {product_id} with image: {image_url}")
#             else:
#                 print(f"❌ No image found for product {product_id}")
#
#
# if __name__ == "__main__":
#     asyncio.run(update_products())
import time

import requests
from pymongo import MongoClient
from config import MONGO_URI

# اتصال به دیتابیس MongoDB
client = MongoClient(MONGO_URI)
db = client["sentiment_analysis_db"]
products_collection = db["products"]


# تابع دریافت تصویر محصول از دیجی‌کالا
def get_digikala_product_image(product_id):
    url = f"https://api.digikala.com/v2/product/{product_id}/"

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'origin': 'https://www.digikala.com',
        'referer': 'https://www.digikala.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'x-web-client': 'desktop',
        'x-web-optimize-response': '1'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            json_data = response.json()
            print(json_data)
            print(url)
            print('[[[[[[[[[[[[[[[[[[[[json_data]]]]]]]]]]]]]]]]]]]]')
            if json_data.get("status") == 200:
                if "images" in json_data["data"]["product"]:
                    main_webp_url = json_data["data"]["product"]["images"]["main"]["webp_url"][0]
                    time.sleep(3)
                    return main_webp_url
                return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching product {product_id}: {e}")

    return ''


# دریافت تمام محصولات از دیتابیس و به‌روزرسانی فیلد 'image'
def update_products():
    for product in products_collection.find():
        product_id = product.get("product_real_id")
        if product_id:
            image_url = get_digikala_product_image(product_id)
            products_collection.update_one({"_id": product["_id"]}, {"$set": {"image": image_url}})
            print(f"✅ Updated product {product_id} with image: {image_url}")

    time.sleep(10)


# اجرای برنامه
if __name__ == "__main__":
    update_products()
