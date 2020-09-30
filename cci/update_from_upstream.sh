#!/usr/bin/env bash

set -e

# Installs & configurations
git config --global user.email "bincrafters@gmail.com"
git config --global user.name "bincrafters-user"


# Install GitHub CLI tool
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0 > /dev/null
sudo apt-add-repository https://cli.github.com/packages
sudo apt-get -qq update
sudo apt-get -qq install gh

# Authenticate on GitHub with the CLI tool
echo ${GIT_GITHUB_TOKEN} | gh auth login --with-token


# Clone the CCI fork
echo ""
git clone "https://${GIT_GITHUB_USERNAME}:${GIT_GITHUB_TOKEN}@github.com/${GIT_GITHUB_FORK_ACCOUNT}/conan-center-index"
cd conan-center-index
echo ""

# Get current master commit
# TODO

###
### Update CCI fork
###
echo ""
git remote add upstream https://github.com/conan-io/conan-center-index
git fetch upstream
git reset --hard upstream/master
git push -f
echo ""

###
### Delete all merged branches in our fork which got merged via a merge commit
###

# TOOD: Debug
git branch -r --merged master

# Get all commit messages between old master commit and newest one 
# TODO

# Isolate the ID of merged PRs from the commit messages
# PR_IDS have to be space separated
# TODO
PR_IDS="2984"

for PR_ID in ${PR_IDS}
do
    # Check if this is a PR from $GIT_GITHUB_FORK_ACCOUNT and also if it is actually meged
    # $'\t' stands for a tab character
    PR_INFORMATION=$(gh pr list --limit 200 --state merged | grep $'\t'"${GIT_GITHUB_FORK_ACCOUNT}:" | grep "${PR_ID}"$'\t')
    echo ${PR_INFORMATION}

    # Retrieve the branch name and delete it
    # TODO
    for segment in ${PR_INFORMATION}
    do
        echo ${segment}
        grep -v "bincrafters:" | sed 's/bincrafters://' | xargs -r -n 1 echo
    done
done

###
### Delete all merged branches in our fork which got NOT merged via a merge commit
###
git branch -r --merged master | grep -v master | sed 's/origin\///' | xargs -r -n 1 git push --delete origin
