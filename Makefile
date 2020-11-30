build-docs:
	make -C docs html

release:
	python setup.py sdist
	twine upload dist/*
