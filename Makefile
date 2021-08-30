.PHONY: pypi-build pypi-test pypi-upload clean

pypi-build: clean
	python setup.py sdist bdist_wheel
	twine check dist/*

pypi-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-upload:
	twine upload dist/*

clean:
	rm -rf build
	rm -rf dist