# Makefile for skeleton
PYTHON = python

all: clean test dist

test:
	@echo "Running skeleton unit tests..."
	@echo ""
	$(PYTHON) -m skeleton.tests.run

build:
	@echo "Build squeleton package..."
	@echo ""
	$(PYTHON) setup.py build

dist: MANIFEST.in
	@echo "Build src distribution of skeleton..."
	@echo ""
	$(PYTHON) setup.py sdist

clean:
	@echo "Remove build and dist directories, and pyc files..."
	@echo ""
	rm -rf ./build/
	rm -rf ./dist/
	find . -name "*.pyc" | xargs rm

MANIFEST.in: .git/objects/*/* .gitignore
	@echo "Update MANIFEST.in..."
	@echo ""
	git ls-files --exclude=".git*" > MANIFEST.in
	@echo ""
