test:
	python3 -m pytest

coverage:
	python3-coverage run tests/test.py
	python3-coverage report

package:
	python3 setup.py bdist_wheel
	rm -rf GRADitude.egg-info
	ls dist/*

build:
	 python3 setup.py bdist

html_doc:
	cd docs && make html && cd ..

show_html_docs:
	firefox docs/build/html/index.html &

pylint:
	pylint bin/graditude graditudelib/* tests/*
