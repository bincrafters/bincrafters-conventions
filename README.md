[![Build Status: Linux and Macos](https://travis-ci.org/uilianries/conan-clang-update.svg?branch=master)](https://travis-ci.org/uilianries/conan-clang-update)
[![Build status: Windows](https://ci.appveyor.com/api/projects/status/github/uilianries/conan-clang-update?svg=true)](https://ci.appveyor.com/project/uilianries/conan-clang-update)
[![codecov](https://codecov.io/gh/uilianries/conan-clang-update/branch/master/graph/badge.svg)](https://codecov.io/gh/uilianries/conan-clang-update)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/conan-clang-update)

# Conan Clang Update

## A script to update Travis CI file

This project contains the script to add Clang 10.0 on OSX builds

#### INSTALL
To install by pip is just one step

##### Local
If you want to install by local copy

    pip install .

##### Remote
Or if you want to download our pip package

    pip install conan_clang_update

#### RUN
To update **ALL** Conan projects on Github https://github.com/uilianries

    $ conan_clang_update --remote=uilianries

To update **ONLY** one project on Github https://github.com/uilianries/conan-libusb

    $ conan_clang_update --remote=uilianries/conan-libusb

To **AVOID** to execute push command after to update

    $ conan_clang_update --remote=uilianries/conan-libusb --skip-push

To filter **PROJECTS** by pattern

    $ conan_clang_update --remote=uilianries --project-pattern uilianries/conan-*

To filter **BRANCHES** by pattern

    $ conan_clang_update --remote=uilianries --branch-pattern stable/*

or

    $ conan_clang_update --remote=uilianries/conan-libzip --branch-pattern stable/*

To update a **LOCAL** file

    $ conan_clang_update --file=.travis.yml


##### Testing and Development
To install extra packages required to test

    pip install .[test]


#### TESTING
To run all unit test + code coverage, just execute:

    pip install -r conan_clang_update/requirements_test.txt
    cd tests
    pytest -v --cov=conan_clang_update


#### REQUIREMENTS and DEVELOPMENT
To develop or run conan clang update

    pip install -r conan_clang_update/requirements.txt


#### UPLOAD
There are two ways to upload this project.

##### Travis CI
After to create a new tag, the package will be uploaded automatically to Pypi.  
Both username and password (encrypted) are in travis file.  
Only one job (python 2.7) will upload, the second one will be skipped.


##### Command line
To upload this package on pypi (legacy mode):

    pip install twine
    python setup.py sdist
    twine upload dist/*


#### LICENSE
[MIT](LICENSE.md)
