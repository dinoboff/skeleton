# Makefile for skeleton
#
# Todo: add help target.


SHELL    = /bin/sh

PYTHON   = python
PYTHON2.6  = python2.6
PYTHON3.1  = python3.1

SETUP        = setup.py
BUILD_CMD    = build
INSTALL_CMD  = install
TEST_CMD     = test
SDIST_CMD    = sdist
BDISTEGG_CMD = bdist_egg
REGISTER_CMD = register
UPLOAD_CMD   = upload


GIT = git

RST2HTML = rst2html.py --strict

VIRTUALENV = virtualenv

DIST_VERSION   = `$(PYTHON) setup.py --version`
RELEASE_BRANCH = release-0.5
RELEASE_REMOTE = origin


all: clean test dist
test-all: test test-py2.6 test-py3.1 test-deploy

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean     To remove temporary build files and compile Python files"
	@echo "  dist      to make skeleton source distribution"
	@echo "  install   to install skeleton"
	@echo "  register  to Create/update skeleton v$(DIST_VERSION) pypi page."
	@echo "  release   to tag and release a new version of skeleton to pypi"
	@echo "  test      to test skeleton with $(PYTHON)"
	@echo "  test-all  to run all tests"
	@echo "  test-deploy"
	@echo "            to test installation of the source distribution"
	@echo "  test-py2.5"
	@echo "            to test skeleton with $(PYTHON2.5)"
	@echo "  test-py2.6"
	@echo "             to test skeleton with $(PYTHON2.6)"
	@echo "  test-py3.1"
	@echo "               to test skeleton with $(PYTHON3.1)"
	@echo "  upload    to upload the source distribution to pypi"
	@echo "            (to use a release got tagged but the upload to pypi failed)"
	@echo "  upload3.1 to upload the Python 3.1 egg to pypi"
	@echo "            (to use a release got tagged but the upload to pypi failed)"
	@echo "  MANIFEST.in"
	@echo "            to make MANIFEST.in from the list of files tracked by git"
	@echo "  README.html"
	@echo "            to make convert README.rst to html and test the result"
	@echo "            in your browser"

build: clean
	@echo "Building squeleton package..."
	$(PYTHON) $(SETUP) $(BUILD_CMD)
	@echo

clean:
	@echo "Removing build and dist directories, and pyc files..."
	rm -rf ./build/
	rm -rf ./dist/
	rm -rf ./v
	rm -f distribute-*.egg
	find . -name "*.pyc" -print0 | xargs -0 rm
	@echo

test-deploy: test-deploy-pip test-deploy-easy_install

test-deploy-pip: dist
	@echo "Test installation of the source distribution with pip."
	rm -rf ./v
	$(VIRTUALENV) --no-site-package ./v
	./v/bin/pip install ./dist/skeleton-*.tar.gz

test-deploy-easy_install: dist
	@echo "Test installation of the source distribution with easy_install."
	rm -rf ./v
	$(VIRTUALENV) --no-site-package ./v
	./v/bin/easy_install ./dist/skeleton-*.tar.gz

dist: clean
	@echo "Building src distribution of skeleton..."
	$(PYTHON) $(SETUP) $(SDIST_CMD)
	@echo

install: clean
	$(PYTHON) $(SETUP) INSTALL_CMD

register: README.html
	@echo "Creating or updating skeleton v$(DIST_VERSION) pypi page."
	$(PYTHON) $(SETUP) $(REGISTER_CMD)

release: clean MANIFEST.in test-all tag upload upload-egg-3.1
	@echo "Version $(DIST_VERSION) released."
	@echo

tag:
	@echo "Tagging version $(DIST_VERSION)..."
	$(GIT) pull $(RELEASE_REMOTE) $(RELEASE_BRANCH)
	$(GIT) tag v$(DIST_VERSION)
	$(GIT) push $(RELEASE_REMOTE) v$(DIST_VERSION)
	@echo

test: clean
	@echo "Running skeleton unit tests..."
	$(PYTHON) $(SETUP) $(TEST_CMD)
	@echo

test-py%: clean
	@echo "Running skeleton unit tests with "$(PYTHON$*)"..."
	rm -rf ./build
	which "$(PYTHON$*)"
	$(PYTHON$*) -c "import sys; sys.version.startswith('$*') or exit(1)"
	$(PYTHON$*) $(SETUP) $(TEST_CMD)
	@echo

upload: test
	@echo "Uploading source distribution to pypi..."
	$(PYTHON) $(SETUP) $(REGISTER_CMD) $(SDIST_CMD) $(UPLOAD_CMD)
	@echo

upload-egg-%: test-py%
	@echo "Uploading to pypi egg distribution for $(PYTHON$*)..."
	$(PYTHON$*) $(SETUP) $(REGISTER_CMD) $(BDISTEGG_CMD) $(UPLOAD_CMD)
	@echo

MANIFEST.in:
	@echo "Update MANIFEST.in..."
	$(GIT) ls-files --exclude=".git*" | sed -e 's/^/include /g' > ./MANIFEST.in
	@echo

README.html: README.rst
	@echo "Making READM.html..."
	$(RST2HTML) README.rst > README.html
	$(PYTHON) -c "import os, webbrowser as w; w.open('file://%s/README.html' % os.getcwd());"

.PHONY: MANIFEST.in clean tag
