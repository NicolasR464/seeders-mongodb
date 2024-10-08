from dotenv import dotenv_values
import os
import sys
import json
import requests
from faker import Faker
from pymongo import MongoClient
import uuid
from datetime import datetime, timedelta, timezone

# Add the project root and utils path to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../utils')))

from utils.pretty_print import print_green

# Load environment variables from .env file
env = dotenv_values(".env")
MULTIAVATAR_API_KEY = env.get('MULTIAVATAR_API_KEY')
MONGO_URI_USER = env.get('MONGO_URI_USER')
OS_CACERT_DIR = env.get('OS_CACERT_DIR')

fake = Faker('fr_FR')

os.environ['SSL_CERT_FILE'] = OS_CACERT_DIR

# MongoDB connections
user_client = MongoClient(MONGO_URI_USER, tls=True, tlsAllowInvalidCertificates=True)

# Access the collections
user_collection = user_client.user_dev.user

# Fetch avatar URL from Multiavatar
def get_avatar_url():
    random_string = uuid.uuid4().hex[:7]
    return f"https://api.multiavatar.com/{random_string}.png?apikey={MULTIAVATAR_API_KEY}"

# Generate fake users
def create_users():
    users = []
    for i in range(100):

        # Use timezone-aware current and past dates
        max_date = datetime.now(timezone.utc)
        min_date = max_date - timedelta(days=730)

        last_connected_str = fake.date_time_between(start_date=min_date, end_date=max_date).isoformat()
        birthday_str = fake.date_time_between(start_date=min_date, end_date=max_date).isoformat()

        user = {
            "version": 1,
            "pseudo": fake.user_name() + "_f",
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
            "sexe": "male" if i % 2 == 0 else "female",
            "birthDate": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),  # ISO 8601
            "rating": fake.random_int(min=0, max=5),
            "phoneNumber": fake.phone_number(),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "postcode": int(fake.postcode()),
                "citycode": int(fake.postcode()[:2]),
                "floor": fake.random_int(min=0, max=10),
                "extra": fake.street_suffix(),
                "geopoints": {
                    "type": "Point",
                    "coordinates": [float(fake.longitude()), float(fake.latitude())]
                }
            },
            "activityStatus": {
                "lastConnected": datetime.strptime(last_connected_str, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone.utc),  
                "birthday": datetime.strptime(birthday_str, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone.utc) 
            },
            "bankInfo": {
                "IBAN": fake.iban(),
                "BIC": fake.swift()
            },
            "avatarUrl": get_avatar_url(),
            "isPremium": fake.boolean(chance_of_getting_true=60),
            "favoriteArticles": [],
            "credit": fake.random_int(min=0, max=500),
            "comments": [],
            "articles": [],
            "debit": []
        }
        users.append(user)
    # Insert users in DB
    user_collection.insert_many(users)

    print_green("Users successfully created!")

# Create users
if __name__ == "__main__":
    create_users()