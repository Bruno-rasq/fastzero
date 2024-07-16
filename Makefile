.PHONY: test

install:
	@pip install -r requirements.txt

run:
	@uvicorn fastzero.app:app --host 0.0.0.0 --port 8080 --reload

test:
	@pytest -v tests