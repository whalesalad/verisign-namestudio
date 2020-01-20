TEST_DIR=tests/

pytest: export ENV=test
pytest:
	python3 -m pytest -x -s -vvvv $(TEST_DIR)
