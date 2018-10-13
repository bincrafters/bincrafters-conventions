#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate conan
fi

python setup.py sdist
pushd tests
pytest -v -s --cov=bincrafters_conventions
mv .coverage ..
popd
