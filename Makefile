docker=docker exec -it python-rss-scrapper_web_1

createsuperuser:
	$(docker) python3 src/manage.py createsuperuser

migrate:
	$(docker) python3 src/manage.py migrate

test:
	$(docker) python3 src/manage.py test

lint:
	@flake8 .
	@isort . --check