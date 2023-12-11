#! /usr/bin/env python3

from perceval.backends.core.git import Git

# url for the git repo to analyze
repo_url = 'https://github.com/raulgc10/OSSanalyzer.git'
# directory for letting Perceval clone the git repo
repo_dir = '/tmp/perceval.git'

# create a Git object, pointing to repo_url, using repo_dir for cloning
repo = Git(uri=repo_url, gitpath=repo_dir)
# fetch all commits as an iterator, and iterate it printing each hash
for commit in repo.fetch():
    print(commit['data']['commit'])