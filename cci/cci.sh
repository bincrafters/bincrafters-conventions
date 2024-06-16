#!/usr/bin/env bash

set -e

if [[ "${REPO_REF}" != "refs/heads/"* ]]; then
  echo "This is not a branch push. Exiting.";
  exit 0 ;
fi

REPO_BRANCH=$(echo $REPO_REF | awk -F '/' '{print $NF}')
echo ${REPO_BRANCH}

git remote rm origin
git remote add origin https://${BOT_GITHUB_NAME}:${BOT_GITHUB_TOKEN}@github.com/${REPO_NAME}.git

git fetch origin master
git fetch origin ${REPO_BRANCH}
git checkout ${REPO_BRANCH}
git push --set-upstream origin ${REPO_BRANCH}

# Is this build triggered by a convention update?
if [[ "$(git log -1 --pretty=%an)" == bincrafters* ]]; then
  echo "This CI run was triggered by a convention update, we don't need to run bincrafters-conventions again";
  exit 0 ;
fi

dirpath="none"
for directory in $(git diff --dirstat=files,0 `git merge-base origin/master ${REPO_BRANCH}`..${REPO_BRANCH} | sed 's/^[ 0-9.]\+% //g'); do
  if [[ "${directory}" == recipes/* ]]; then
    count=$(echo "${directory}" | awk -F"/" '{print NF-1}');
    if [[ "${count}" -ge "3" ]]; then
      dirpath="${directory}"
    fi;
  fi;
done


if [[ "${dirpath}" == "none" ]]; then
  echo "This branch didn't change any recipe. Exiting.";
  exit 0 ;
fi

recipename=${dirpath#*recipes/}
recipename=${recipename%%/*}
recipepath="recipes/${recipename}/"
version=${dirpath#"$recipepath"}
version=${version%%/*}
recipepath="recipes/${recipename}/${version}"

echo ${recipename}

echo ${recipepath}
cd ${recipepath}


git config --global user.email "${BOT_GITHUB_EMAIL}"
git config --global user.name "${BOT_GITHUB_NAME}"

pip install --quiet bincrafters-conventions
conan user  # initialize Conan registry file

bincrafters-conventions


git add -u 
git reset -- cci.sh

git diff-index --quiet HEAD || git commit -a -m "${recipename}: Update Conan conventions" -m "Automatically created by $(bincrafters-conventions --version)" && git push
