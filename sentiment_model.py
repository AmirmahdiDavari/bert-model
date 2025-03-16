# from transformers import pipeline
#
# sentiment_pipeline = pipeline("text-classification", model="HooshvareLab/bert-fa-base-uncased-sentiment")
#
#
# def analyze_sentiment(text: str) -> str:
#     result = sentiment_pipeline(text)
#     return result[0]["label"].lower()  # خروجی می‌تواند "positive"، "neutral" یا "negative" باشد
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load ParsBERT model and tokenizer directly
tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased-sentiment-digikala")
model = AutoModelForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased-sentiment-digikala")

# Sentiment labels
labels = ["منفی", "خنثی", "مثبت"]


async def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Ensure that the model does not track gradients
    with torch.no_grad():
        outputs = model(**inputs)

    # Get softmax probabilities
    scores = outputs.logits.softmax(dim=-1).tolist()[0]
    sentiment = labels[scores.index(max(scores))]  # Get the highest score label

    return sentiment, scores


# # Example Test
# text =  "این محصول  خوب  است  "
# sentiment, scores = analyze_sentiment(text)
#
# print(f"🔹 متن: {text}")
# print(f"📌 احساسات: {sentiment}")
# print(f"📊 امتیازات: {scores}")
