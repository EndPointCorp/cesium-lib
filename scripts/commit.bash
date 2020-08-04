#!/bin/bash

echo "read version"

tag=`cat latest/version.txt`
echo "Version: ${tag}"

git add -A
git commit -m "Cesium ${tag} release"
git tag ${tag}
git push --tags
