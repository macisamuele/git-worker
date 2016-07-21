#!/bin/bash

mkdir -p /gitlab-git-http-server/test/data/
cd /gitlab-git-http-server/test/data/

mkdir test.git
cd test.git
git init --bare
