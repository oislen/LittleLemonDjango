:: make db migrations and import data
call uv run python manage.py makemigrations restaurant
call uv run python manage.py migrate
call uv run python manage.py runscript restaurant.import_data