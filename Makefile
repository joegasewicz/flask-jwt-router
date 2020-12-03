build-docs:
	make -C docs html

release:
	python setup.py sdist
	twine upload dist/* --verbose

python-tests:
	tox

test:
	pipenv run pytest -vv

install:
	pipenv install
	pipenv install --dev
