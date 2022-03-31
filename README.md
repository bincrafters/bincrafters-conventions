![Build status](https://github.com/bincrafters/bincrafters-conventions/workflows/conventions/badge.svg)
[![Codecov](https://codecov.io/gh/bincrafters/bincrafters-conventions/branch/main/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-conventions)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/bincrafters-conventions)

# Bincrafters Conventions

## A Script to update Conan projects following Conan conventions

This project contains scripts to update CI files, to
update Conan conventions in general and to perform some linting.

### INSTALL

You can install `bincrafters-conventions` via `pip` like this:

    $ pip install bincrafters_conventions

### RUN

> 💡 Bincrafters Conventions is a command line tool.
> 
> Execute `bincrafters-conventions --help` to see all options.
> 
> `bincrafters-conventions` has also the alias `bcon` for convince.


#### EXAMPLES

To update **ALL** Conan projects on GitHub for https://github.com/bincrafters

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

To apply Conan conventions in a local file:

    $ bincrafters_conventions --conanfile=conanfile.py

To update AppVeyor file:

    $ bincrafters_conventions --appveryorfile=appveyor.yml


### Testing and Development

If you want to install `bincrafters-conventions` via a local git clone

    pip install --user -U .

To install extra packages required to test

    pip install .[test]

To run all unit test + code coverage, execute:

    cd tests
    pytest -v --cov=bincrafters_conventions


### LICENSE

[MIT](LICENSE.md)
