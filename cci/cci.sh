#!/usr/bin/env bash

set -e

git diff --dirstat=files,0 `git merge-base master ${APPVEYOR_REPO_BRANCH}`..${APPVEYOR_REPO_BRANCH}


# Install & configuration
git config --global user.email "bincrafters@gmail.com"
git config --global user.name "bincrafters-user"
pip install --quiet bincrafters-conventions
conan user  # initialize Conan registry file
