.PHONY: test compile-handlebars jasmine-ci jasmine-browser lint

JS_TEST_BROWSER?=phantomjs

help:
	@echo "test - run the jasmine test suite"
	@echo "compile-handlebars - compile the handlebars templates"
	@echo "lint - check style with jshint"

test: compile-handlebars jasmine-ci

test-browser: compile-handlebars jasmine-browser

jasmine-ci:
	jasmine-ci --browser=$(JS_TEST_BROWSER)

jasmine-browser:
	jasmine

compile-handlebars:
	handlebars ../volunteer/static/js/shift-grid/templates -f compiled/templates.js

lint:
	jshint ../volunteer/static/js/shift-grid/
