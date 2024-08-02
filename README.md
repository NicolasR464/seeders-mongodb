# MongoDB Seeder Project

This project contains scripts for seeding MongoDB collections with fake data for development and testing purposes. The project is organized into multiple directories for managing user and article collections separately.

## Activate the python environment on macOs and Linux:

```bash
python -m venv venv
source venv/bin/activate
```

## Or activate the python environment on Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

## Then install Python libs:

```bash
pip install -r requirements.txt
```

## Create a .env file, add these values:

```bash
PEXELS_API_KEY=<your_pexels_api_key>
MULTIAVATAR_API_KEY=<your_multiavatar_api_key>
MONGO_URI_USER=<your_mongo_uri_for_user_database>
MONGO_URI_ARTICLE=<your_mongo_uri_for_article_database>
OS_CACERT_DIR=<path_to_your_cacert.pem_file>
```

## Usage

To create fake users in the database: `make create_users`

Create Articles: `make create_articles`

Delete All Documents: `make delete_all`

## Notes

> Make sure the API keys and MongoDB URIs are correctly set in the .env file.

> If you have connection issues to MongoDB, you might need to download a cacert.pem file from the official [cURL website](https://curl.se/ca/cacert.pem)

> The scripts use [Pexels API](https://www.pexels.com/fr-fr/api/documentation/#guidelines) (limited to 200 requests per hour) to fetch image URLs and the [Multiavatar API](https://multiavatar.com/) to generate avatar URLs.
