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
# TODO:
# > 17. Sep
OLD_COMMIT=$(git rev-parse HEAD)
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
### The first instinct might be that the list of "recently merged PR IDs from user X"
### might already be enough and the parsing of other information is unnecessary.
### However, it is not. Branch names can and will get recyceled. 
### Only using this single list would cause deletion of still unmerged branches.
###
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
PR_IDS=""
while read COMMIT_MESSAGE
do
    NEW_ID=$(echo "$COMMIT_MESSAGE" | sed -nr 's/(.*)\(#([0-9]*)\)(.*)/\2/p');
    if [[ ! "${NEW_ID}" == "" ]]; then
        if [[ "${PR_IDS}" == "" ]]; then
            PR_IDS="${NEW_ID}";
        else
            PR_IDS="${PR_IDS} ${NEW_ID}";
        fi;
    fi;
done  < <(echo "${COMMIT_MESSAGES}")

echo "Detected IDs of the PR who got merged, based on the new commits:"
echo "${PR_IDS}"

echo ""
echo "Recently merged PR IDs from ${GIT_GITHUB_FORK_ACCOUNT}, according to the API:"
RECENT_PRS=$(gh pr list --limit 200 --state merged | grep $'\t'"${GIT_GITHUB_FORK_ACCOUNT}:")
echo "${RECENT_PRS}"
echo ""

echo ""
echo "Matching commit and API based information"
echo "Delete all merged branches, which got merged via a merge commit:"
for PR_ID in ${PR_IDS}
do
    # Check if this is a PR from $GIT_GITHUB_FORK_ACCOUNT and also if it is actually meged
    # ^ because the PR ID should match the beginning of the string
    # $'\t' stands for a tab character
    # || true because the CI should not "fail" when the last PR is not a PR from $GIT_GITHUB_FORK_ACCOUNT
    PR_INFORMATION=$(echo "${RECENT_PRS}" | grep "^${PR_ID}"$'\t') || true
    if [[ ! "${PR_INFORMATION}" == "" ]]; then 
        echo "Found match: ${PR_INFORMATION}"

        # Retrieve the branch name and delete it
        # -n to not get any output if there is (no) match
        # -r to enable extend regex syntax
        # /p to print matches despite -n
        BRANCH_NAME=$(echo "${PR_INFORMATION}" | sed -nr 's/([0-9]*)\t(.*)\t(.*)'"${GIT_GITHUB_FORK_ACCOUNT}:"'(.*)\t(.*)/\4/p')
        if [[ ! "${BRANCH_NAME}" == "" ]]; then 
            echo "Delete branch: ${BRANCH_NAME}"
            echo "${BRANCH_NAME}" | xargs -r -n 1 git push --delete origin
            echo ""
        fi
    fi
done

###
### Delete all merged branches in our fork which got NOT merged via a merge commit
###
echo ""
echo ""
echo "Delete all merged branches, which got merged, but NOT via a merge commit:"
git branch -r --merged master | grep -v master | sed 's/origin\///' | xargs -r -n 1 git push --delete origin
echo ""
