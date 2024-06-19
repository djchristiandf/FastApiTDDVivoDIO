run:
	@uvicorn store.main:app --reload

precommit-install:
	@poetry run pre-commit install

test:
	@poetry run pytest

test-matching:
	@poetry run pytest -s -rx -k $(K) --pdb store ./tests/

test-create:
	@poetry run pytest -s -rx -k test_usecases_create_should_return_success --pdb store ./tests/

test-get:
	@poetry run pytest -s -rx -k test_usecases_get_should_return_success --pdb store ./tests/

test-update:
	@poetry run pytest -s -rx -k test_usecases_update_should_return_success --pdb store ./tests/
