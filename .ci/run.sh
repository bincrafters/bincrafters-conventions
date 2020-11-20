#!/usr/bin/env bash

set -ex

python setup.py sdist
pushd tests
pytest -v -s --cov=bincrafters_conventions
mv .coverage ..
popd
