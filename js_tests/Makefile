.PHONY: test compile-handlebars jasmine-ci jasmine-browser lint

help:
	@echo "test - run the mocha test suite"
	@echo "compile-handlebars - compile the handlebars templates"
	@echo "lint - check style with jshint"

test: compile-handlebars mocha-ci

test-browser: compile-handlebars

mocha-ci:
	mocha-phantomjs index.html
	

compile-handlebars:
	handlebars ../volunteer/static/js/shift-grid/templates -f compiled/templates.js

lint:
	jshint ../volunteer/static/js/shift-grid/
	jshint tests/
