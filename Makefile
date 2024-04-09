SRC_DIR := cd src;  # All commands must be run on src/ directory

makemigrations:
	$(SRC_DIR) python manage.py makemigrations

migrate:
	$(SRC_DIR) python manage.py migrate

runserver:
	$(SRC_DIR) python manage.py runserver

test:
	$(SRC_DIR) pytest --ds=thebook.settings -s
