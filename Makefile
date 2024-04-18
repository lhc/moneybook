SRC_DIR := cd src;  # All commands must be run on src/ directory

makemigrations:
	$(SRC_DIR) python manage.py makemigrations

migrate:
	$(SRC_DIR) python manage.py migrate

runserver:
	$(SRC_DIR) python manage.py runserver

shell:
	$(SRC_DIR) python manage.py shell

test:
	$(SRC_DIR) pytest --ds=thebook.settings -s
