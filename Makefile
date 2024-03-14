init:
	alembic upgrade head
	python create_super_user.py admin@example.com 1234

run: init
	python main.py

run_tests:
	pytest tests