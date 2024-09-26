#!/bin/zsh
source ~/.zshrc

BASEDIR=$(pwd)

rsync -avhL --delete --exclude-from 'exclude-list.txt' "$BASEDIR"/ mksachs@iad1-shared-b8-17.dreamhost.com:mikesachs.com
