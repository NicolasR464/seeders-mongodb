.PHONY: create_users create_articles delete_all

create_users:
	python3 collections/users/create_users.py

create_articles:
	python3 collections/articles/create_articles.py

delete_all:
	python3 collections/delete_all.py