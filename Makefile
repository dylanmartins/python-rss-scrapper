docker=docker exec -it python-rss-scrapper_web_1

createsuperuser:
	$(docker) python3 src/manage.py createsuperuser

makemigrations:
	$(docker) python3 src/manage.py makemigrations

migrate:
	$(docker) python3 src/manage.py migrate

test:
	$(docker) py.test -vv -xs src

lint:
	@flake8 .
	@isort . --check