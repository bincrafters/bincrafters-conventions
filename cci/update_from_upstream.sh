#!/usr/bin/env bash

set -e

# Installs & configurations
git config --global user.email "bincrafters@gmail.com"
git config --global user.name "bincrafters-user"


# Install GitHub CLI tool
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0 > /dev/null
sudo apt-add-repository https://cli.github.com/packages > /dev/null
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
# > 17. Sep
OLD_COMMIT="808a5eec296dff148585c8e5f55428b52c50143b"

###
### Update CCI fork
###
echo ""
echo "Updating the CCI fork"
git remote add upstream https://github.com/conan-io/conan-center-index
git fetch upstream
git reset --hard upstream/master
git push -f
echo ""

###
### Delete all merged branches in our fork which got merged via a merge commit
###
### General notes: 
### Some checks in this section might be interpreted as duplicates on first sight,
### but those are considered to be safe guards for edge cases.
### In fact, highly theoretically it is possible for outsiders
### to deleted branches in our fork, by writing specific targeted PR titles
### and then getting this PR merged within a short, specific time period.
### However, this would still need to pass the reviews, the very short time window
### makes it almost impossible and the worst case is that we have to restore a branch manually. 
### tl;dr: We should be fine.

# Get all commit messages between old master commit and newest one
echo ""
echo "All new commits:"
COMMIT_MESSAGES=$(git log --pretty='format:%s' --abbrev-commit --ancestry-path ${OLD_COMMIT}..HEAD)
echo "${COMMIT_MESSAGES}"
echo ""

# Isolate the ID of merged PRs from the commit messages
# PR_IDS have to be space separated
# TODO
PR_IDS=""
for COMMIT_MESSAGE in ${COMMIT_MESSAGES}
do
    if [[ "${COMMIT_MESSAGE}" == "(#"* ]]; then 
        NEW_ID=$(echo "$COMMIT_MESSAGE" | sed -r 's/\(#([0-9]*)\).*/\1/g')
        if [[ "${PR_IDS}" == "" ]]; then
            PR_IDS="${NEW_ID}"
        else
            PR_IDS="${PR_IDS} ${NEW_ID}"
        fi
    fi
done
# PR_IDS="2984"
echo "${PR_IDS}"

echo ""
echo "Delete all merged branches, which got merged via a merge commit"
RECENT_PRS=$(gh pr list --limit 200 --state merged | grep $'\t'"${GIT_GITHUB_FORK_ACCOUNT}:")
echo "Recently merged PR IDs from ${GIT_GITHUB_FORK_ACCOUNT}:"
PR_INFORMATION="$(echo "${RECENT_PRS}" | grep "${PR_ID}"$'\t')"
echo "${PR_INFORMATION}"
echo "${RECENT_PRS}"

for PR_ID in "${PR_IDS}"
do
    # Check if this is a PR from $GIT_GITHUB_FORK_ACCOUNT and also if it is actually meged
    # $'\t' stands for a tab character
    PR_INFORMATION="$(echo "${RECENT_PRS}" | grep "${PR_ID}"$'\t')"
    echo "${PR_INFORMATION}"

    # Retrieve the branch name and delete it
    # TODO
    # BRANCH_NAME=$(echo "${PR_INFORMATION}" | sed -r $'s/([0-9]*\t.*\t.*'"${GIT_GITHUB_FORK_ACCOUNT}:"$'(.*)\t.*/\1/g')
    # -n to not get any output if there is (no) match
    # -r to enable extend regex syntax
    # /p to print matches despite -n
    # BRANCH_NAME=$(echo "${PR_INFORMATION}" | sed -nr 's/([0-9]*)\t(.*)\t(.*)'"${GIT_GITHUB_FORK_ACCOUNT}:"'(.*)\t(.*)/\4/p')
    # echo "${PR_INFORMATION}" | sed -nr 's/([0-9]*)\t(.*)\t(.*)'"${GIT_GITHUB_FORK_ACCOUNT}:"'(.*)\t(.*)/\4/p' | xargs -r -n 1 echo
done

###
### Delete all merged branches in our fork which got NOT merged via a merge commit
###
# echo ""
# echo "Delete all merged branches, which got merged, but NOT via a merge commit"
# git branch -r --merged master | grep -v master | sed 's/origin\///' | xargs -r -n 1 git push --delete origin
