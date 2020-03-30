#!/usr/bin/env bash

set -e

git remote rm origin
git remote add origin https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/bincrafters/conan-center-index.git

git fetch origin master
git fetch origin ${APPVEYOR_REPO_BRANCH}
git checkout ${APPVEYOR_REPO_BRANCH}
git push --set-upstream origin ${APPVEYOR_REPO_BRANCH}

# Is this build triggered by a convention update?
if [[ "$(git log -1 --pretty=%an)" == bincrafters* ]]; then
  echo "This CI run was triggered by a convention update, we don't need to run bincrafters-conventions again";
  exit 0 ;
fi

dirpath="none"
for directory in $(git diff --dirstat=files,0 `git merge-base origin/master ${APPVEYOR_REPO_BRANCH}`..${APPVEYOR_REPO_BRANCH} | sed 's/^[ 0-9.]\+% //g'); do
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

# Install & configuration
unset PYENV_ROOT;
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash;
export PATH="$HOME/.pyenv/bin:$PATH";
eval "$(pyenv init -)";
eval "$(pyenv virtualenv-init -)";
pyenv --version;
pyenv install 3.7.7;
pyenv virtualenv 3.7.7 conan;
pyenv rehash;
pyenv activate conan;

python --version
pip --version

git config --global user.email "bincrafters@gmail.com"
git config --global user.name "bincrafters-user"

pip install --quiet bincrafters-conventions
conan user  # initialize Conan registry file

bincrafters-conventions


git add -u 
git reset -- cci.sh

git diff-index --quiet HEAD || git commit -a -m "${recipename}: Update Conan conventions" -m "Automatically created by $(bincrafters-conventions --version)" && git push
