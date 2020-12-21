docker=docker exec -it src_web_1

createsuperuser:
	$(docker) python3 manage.py createsuperuser

makemigrations:
	$(docker) python3 manage.py makemigrations

migrate:
	$(docker) python3 manage.py migrate

test:
	$(docker) py.test -vv -xs .

lint:
	@flake8 .
	@isort . --check