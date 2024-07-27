from dotenv import dotenv_values
import os
import sys
from pymongo import MongoClient

# Add the project root and utils path to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))

from utils.pretty_print import print_green, print_red

# Load environment variables from .env file
env = dotenv_values(".env")
MONGO_URI_USER = env.get('MONGO_URI_USER')
MONGO_URI_ARTICLE = env.get('MONGO_URI_ARTICLE')
OS_CACERT_DIR = env.get('OS_CACERT_DIR')

os.environ['SSL_CERT_FILE'] = OS_CACERT_DIR

# MongoDB connections
user_client = MongoClient(MONGO_URI_USER, tls=True, tlsAllowInvalidCertificates=True)
article_client = MongoClient(MONGO_URI_ARTICLE, tls=True, tlsAllowInvalidCertificates=True)

# Access the collections
user_collection = user_client.user_dev.user
article_collection = article_client.article_dev.article

# Delete all documents from collections
def delete_all_documents():
    user_collection.delete_many({})
    article_collection.delete_many({})
    print_green("All documents deleted from user and article collections")

# Execute deletion
if __name__ == "__main__":
    delete_all_documents()