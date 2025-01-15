#!/bin/bash

# Exit if something fails
set -e


if [[ -z "$XDG_DATA_HOME" ]]; then
    prefix=~/.local/share
else
    prefix="$XDG_DATA_HOME"
fi

mkdir -p $prefix/krunner/dbusplugins/
mkdir -p $prefix/dbus-1/services/

cp plasma-runner-krha.desktop $prefix/krunner/dbusplugins/
sed "s|/home/qbit/projects/krha/krha.py|${PWD}/krha.py|" "org.kde.krha.service" > $prefix/dbus-1/services/org.kde.krha.service

kquitapp5 krunner

