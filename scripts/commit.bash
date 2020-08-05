#!/bin/bash

echo "read version"

tag=`cat latest/version.txt`
echo "Version: ${tag}"

eval $(ssh-agent -s)


if git rev-parse ${tag} >/dev/null 2>&1
then
    echo "Tag ${tag} already exists"
else
    git add -A
    git commit -m "Cesium ${tag} release"
    git tag ${tag}
    git push --tags origin master
fi

