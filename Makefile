# Makefile for skeleton
#
# Todo: add help target.


srcdir = .
setupoptions = 
buildoptions = 
sdistoptions = 
installoptions = 
testoptions = 
uploadoptions = 
registeroptions = 


SHELL = /bin/sh
PYTHON_BIN = python
PYTHON_BIN3 = python3
PYTHON = PYTHONPATH="$(srcdir)/" $(PYTHON_BIN)
PYTHON3 = PYTHONPATH="$(srcdir)/" $(PYTHON_BIN3)
SETUP = $(PYTHON) $(srcdir)/setup.py $(setupoptions)
SETUP3 = $(PYTHON3) $(srcdir)/setup.py $(setupoptions)
GIT_BIN = git
RELEASE_BRANCH = release-0.3
GIT_DIR = $(srcdir)/.git
GIT_WORK_TREE = $(srcdir)
GIT = $(GIT_BIN) --git-dir="$(GIT_DIR)" --work-tree="$(GIT_WORK_TREE)"

DIST_VERSION = `$(PYTHON) setup.py --version`

all: clean test dist

build:
	@echo "Building squeleton package..."
	$(SETUP) build $(buildoptions)
	@echo

clean:
	@echo "Removing build and dist directories, and pyc files..."
	rm -rf ./build/
	rm -rf ./dist/
	rm -f distribute-*.tar.gz
	rm -f distribute-*.egg
	find $(srcdir) -name "*.pyc" -print0 | xargs -0 rm
	@echo

dist: MANIFEST
	@echo "Building src distribution of skeleton..."
	$(SETUP) sdist $(sdistoptions)
	@echo

install:
	$(SETUP) install $(installoptions)

release: clean test tag upload
	@echo "Version $(DIST_VERSION) released."
	@echo

tag:
	@echo "Tagging version $(DIST_VERSION)..."
	$(GIT) pull origin $(RELEASE_BRANCH)
	$(GIT) tag v$(DIST_VERSION)
	$(GIT) push origin v$(DIST_VERSION)
	@echo

test: clean
	@echo "Running skeleton unit tests..."
	$(SETUP) test $(testoptions)
	@echo

test3: clean
	@echo "Running skeleton unit tests with Python 3..."
	$(SETUP3) test $(testoptions)
	@echo

upload: MANIFEST
	@echo "Uploading source distribution to pypi..."
	$(SETUP) register $(registeroptions) sdist $(sdistoptions) upload $(uploadoptions)
	@echo
	
upload3: MANIFEST clean
	@echo "Uploading source distribution to pypi..."
	$(SETUP3) test $(testoptions)
	$(SETUP3) register $(registeroptions) bdist_egg $(sdistoptions) upload $(uploadoptions)
	@echo

MANIFEST:
	@echo "Update MANIFEST.in..."
	$(GIT) ls-files --exclude=".git*" | sed -e 's/^/include /g' > $(srcdir)/MANIFEST.in
	@echo
