:: clear website cache data
call exeClearData.cmd
:: make db migrations and import data
call exeLoadData.cmd
:: run django app test
call exeUnitTests.cmd
:: run web-app
call uv run python manage.py runserver