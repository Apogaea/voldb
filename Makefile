.PHONY: js-test bower-install mocha-ci compile-handlebars js-lint

help:
	@echo "test - run the mocha test suite"
	@echo "compile-handlebars - compile the handlebars templates"
	@echo "lint - check style with jshint"

js-test: bower-install compile-handlebars mocha-ci

bower-install:
	bower install

mocha-ci:
	mocha-phantomjs js_tests/index.html

compile-handlebars:
	handlebars volunteer/static/js/shift-grid/templates -f js_tests/compiled/templates.js

js-lint:
	jshint volunteer/static/js/shift-grid/
	jshint js_tests/tests/
