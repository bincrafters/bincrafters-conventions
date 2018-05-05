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
pytest -v --cov=conan_clang_update
mv .coverage ..
popd
