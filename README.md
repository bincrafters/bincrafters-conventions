[![Build Status: Linux and macOS](https://travis-ci.org/bincrafters/bincrafters-conventions.svg?branch=master)](https://travis-ci.org/bincrafters/bincrafters-conventions)
[![Build status: Windows](https://ci.appveyor.com/api/projects/status/github/bincrafters/bincrafters-conventions?svg=true)](https://ci.appveyor.com/project/bincrafters/bincrafters-conventions)
[![codecov](https://codecov.io/gh/bincrafters/bincrafters-conventions/branch/master/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-conventions)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/bincrafters-conventions)

# Bincrafters Conventions

## A Script to update Conan projects following Conan conventions

This project contains the script to add new compiler versions in Travis file and update Conan conventions

#### Motivation

- https://github.com/bincrafters/community/issues/482

#### INSTALL
To install by pip is just one step

##### Local
If you want to install by local copy

    pip install .

##### Remote
Or if you want to download our pip package

    pip install bincrafters_conventions

#### RUN
To update **ALL** Conan projects on Github https://github.com/bincrafters

    $ bincrafters_conventions --remote=bincrafters

To update **ONLY** one project on Github https://github.com/bincrafters/conan-conversion

    $ bincrafters_conventions --remote=bincrafters/conan-double-conversion

To **AVOID** to execute push command after to update

    $ bincrafters_conventions --remote=bincrafters/conan-libusb --dry-run

To filter **PROJECTS** by pattern

    $ bincrafters_conventions --remote=bincrafters --project-pattern bincrafters/conan-*

To filter **BRANCHES** by pattern

    $ bincrafters_conventions --remote=bincrafters --branch-pattern stable/*

or

    $ bincrafters_conventions --remote=bincrafters/conan-libzip --branch-pattern stable/*

To update and check **LOCAL** everything

    $ bincrafters_conventions
    
To check **LOCAL** everything

    $ bincrafters_conventions --check
    
To update a **LOCAL** file

    $ bincrafters_conventions --travisfile=.travis.yml

To apply Conan conventions in a local file:

    $ bincrafters_conventions --conanfile=conanfile.py

To update appveyor file:

    $ bincrafters_conventions --appveryorfile=appveyor.yml


##### Testing and Development
To install extra packages required to test

    pip install .[test]


#### TESTING
To run all unit test + code coverage, just execute:

    pip install -r bincrafters_conventions/requirements_test.txt
    cd tests
    pytest -v --cov=bincrafters_conventions


#### REQUIREMENTS and DEVELOPMENT
To develop or run conan clang update

    pip install -r bincrafters_conventions/requirements.txt


#### UPLOAD
There are two ways to upload this project.

##### Travis CI
After to create a new tag, the package will be uploaded automatically to Pypi.  
Both username and password (encrypted) are in travis file.  


##### Command line
To upload this package on pypi (legacy mode):

    pip install twine
    python setup.py sdist
    twine upload dist/*


#### LICENSE
[MIT](LICENSE.md)
