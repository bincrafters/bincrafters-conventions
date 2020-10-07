[![Build Status: Linux and macOS](https://travis-ci.com/bincrafters/bincrafters-conventions.svg?branch=main)](https://travis-ci.com/bincrafters/bincrafters-conventions)
[![Build status: Windows](https://ci.appveyor.com/api/projects/status/github/bincrafters/bincrafters-conventions?svg=true)](https://ci.appveyor.com/project/bincrafters/bincrafters-conventions)
[![codecov](https://codecov.io/gh/bincrafters/bincrafters-conventions/branch/main/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-conventions)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/bincrafters-conventions)

# Bincrafters Conventions

## A Script to update Conan projects following Conan conventions

This project contains scripts to update CI files, to
update Conan conventions in general and to perform some linting.

#### INSTALL
To install by pip is just one step

##### Local
If you want to install via a local git clone

    pip install .

##### Remote
Or if you want to install a release version

    pip install bincrafters_conventions

#### RUN
To update **ALL** Conan projects on GitHub https://github.com/bincrafters

    $ bincrafters_conventions --remote=bincrafters

To update **ONLY** one project on GitHub https://github.com/bincrafters/conan-conversion

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

To update AppVeyor file:

    $ bincrafters_conventions --appveryorfile=appveyor.yml


##### Testing and Development
To install extra packages required to test

    pip install .[test]


#### TESTING
To run all unit test + code coverage, execute:

    pip install .[test]
    cd tests
    pytest -v --cov=bincrafters_conventions


#### REQUIREMENTS and DEVELOPMENT
To develop or run bincrafters-conventions:

    pip install --user -U .
    bincrafters-conventions

#### LICENSE
[MIT](LICENSE.md)
