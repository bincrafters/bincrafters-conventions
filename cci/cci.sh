#!/usr/bin/env bash

set -e

echo ${APPVEYOR_REPO_BRANCH}

git fetch origin master
git fetch origin ${APPVEYOR_REPO_BRANCH}

git checkout ${APPVEYOR_REPO_BRANCH}

for directory in $(git diff --dirstat=files,0 `git merge-base origin/master ${APPVEYOR_REPO_BRANCH}`..${APPVEYOR_REPO_BRANCH} | sed 's/^[ 0-9.]\+% //g'); do
  if [[ "${directory}" == recipes/* ]]; then
    count=$(echo "${directory}" | awk -F"/" '{print NF-1}');
    if [[ "${count}" == "3" ]]; then
      path="${directory}"
    fi;
  fi;
done

echo ${path}
cd ${path}


# Install & configuration
unset PYENV_ROOT;
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash;
export PATH="$HOME/.pyenv/bin:$PATH";
eval "$(pyenv init -)";
eval "$(pyenv virtualenv-init -)";
pyenv --version;
pyenv install 3.7.5;
pyenv virtualenv 3.7.5 conan;
pyenv rehash;
pyenv activate conan;

python --version
pip --version

git config --global user.email "bincrafters@gmail.com"
git config --global user.name "bincrafters-user"

git remote rm origin
git remote add origin https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/bincrafters/conan-center-index.git

pip install --quiet bincrafters-conventions
conan user  # initialize Conan registry file

bincrafters-conventions


git add -A

git commit -am 'Update Conan conventions

Automatically created by $(bincrafters-conventions--version)'

git push
