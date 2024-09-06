from dotenv import dotenv_values
import os
import sys
import json
import requests
from faker import Faker
from pymongo import MongoClient
import uuid
from datetime import datetime,timezone


# Add the project root and utils path to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../utils')))

from mocks import categories
from utils.pretty_print import print_green, print_red

# Load environment variables from .env file
env = dotenv_values(".env")
PIXABAY_API_KEY = env.get('PIXABAY_API_KEY')
MONGO_URI_USER = env.get('MONGO_URI_USER')
MONGO_URI_ARTICLE = env.get('MONGO_URI_ARTICLE')
OS_CACERT_DIR = env.get('OS_CACERT_DIR')


fake = Faker('fr_FR')

os.environ['SSL_CERT_FILE'] = OS_CACERT_DIR

# MongoDB connection
article_client = MongoClient(MONGO_URI_ARTICLE, tls=True, tlsAllowInvalidCertificates=True)
user_client = MongoClient(MONGO_URI_USER, tls=True, tlsAllowInvalidCertificates=True)

# Access the collections
article_collection = article_client.article_dev.article
user_collection = user_client.user_dev.user

# Fetch Pixabay image URLs for product photos
def get_pixabay_image_urls(category):
    params = {
        'key': PIXABAY_API_KEY,
        'q': category,
        'image_type': 'photo',
        'per_page': 3
    }
    response = requests.get('https://pixabay.com/api/', params=params)
    
    if response.status_code != 200:
        print_red(f"Failed to fetch images from Pixabay API: {response.status_code}")
        print(response.text)  # Print the response text for more details
        return []
    
    data = response.json()

    if 'hits' not in data:
        print_red(f"Unexpected response structure: {data}")
        return []

    return [hit['userImageURL'] for hit in data['hits']]


# Generate fake articles
def create_articles():
    articles = []
    user_ids = [user["_id"] for user in user_collection.find({}, {"_id": 1})]  

    if not user_ids:
        print("\033[91m{}\033[00m".format("No users found. Cannot create articles without users."))
      
        return

    for i in range(40):
        category = fake.random_element(elements=list(categories.keys()))
        subCategory = fake.random_element(elements=categories[category])
        images = get_pixabay_image_urls(category)
        article = {
            "version": 1,
            "owner": fake.random_element(elements=user_ids), 
            "adTitle": fake.catch_phrase(),
            "brand": fake.company(),
            "model": fake.word(),
            "description": fake.text(),
            "status": "available",
            "state": "used",
            "price": fake.random_int(min=10, max=1000),
            "manufactureDate": fake.date_this_century().isoformat(),
            "purchaseDate": fake.date_this_year().isoformat(),
            "imageUrls": images,
            "createdAt": datetime.now(timezone.utc).isoformat(),  
            "lastModified":datetime.now(timezone.utc).isoformat(), 
            "category": category,
            "subCategory": subCategory,
            "deliveryType": ["pickup"],
            "dimensions": {
                "length": fake.random_int(min=1, max=100),
                "width": fake.random_int(min=1, max=100),
                "height": fake.random_int(min=1, max=100),
                "weight": fake.random_int(min=1, max=100)
            }
        }
        articles.append(article)
        
    # Insert articles in DB
    article_collection.insert_many(articles)

    print_green("Articles successfully created!")

# Create articles
if __name__ == "__main__":
    create_articles()