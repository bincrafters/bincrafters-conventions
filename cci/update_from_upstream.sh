#!/usr/bin/env bash

set -e

# Installs & configurations
git config --global user.email "bincrafters@gmail.com"
git config --global user.name "bincrafters-user"
conan user  # initialize Conan registry file


# Update Bincrafters' fork of Conan Center Index
git clone "https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/bincrafters/conan-center-index"
cd conan-center-index
git remote add upstream https://github.com/conan-io/conan-center-index
git fetch upstream
git reset --hard upstream/master
git push -f


# Delete all merged branches in our fork 
git branch -r --merged master | grep -v master | sed 's/origin\///' | xargs -r -n 1 git push --delete origin
