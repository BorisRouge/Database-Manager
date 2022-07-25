#!/bin/sh
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/BorisRouge/Database-Manager.git
git push -u origin main