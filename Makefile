.PHONY: clean-pyc clean-build docs

help:
	@echo "docs - generate Sphinx HTML documentation, including API docs"

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html
