#! /usr/bin/env bash

pyxel package . run.py
pyxel app2html snake_pyxel.pyxapp
mv snake_pyxel.html index.html

git checkout master
git add .
git commit
git push
git checkout release
git merge master
git push

