#!/usr/bin/env bash

set -ex

pip install codecov
pip install -e .[test]
