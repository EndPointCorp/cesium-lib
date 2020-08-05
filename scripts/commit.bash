#!/bin/bash

echo "read version"

tag=`cat latest/version.txt`
echo "Version: ${tag}"

eval $(ssh-agent -s)

git add -A
git commit -m "Cesium ${tag} release"
git tag ${tag}
git push --tags

git push origin master
