#!/bin/bash

# Exit if something fails
set -e

if [[ -z "$XDG_DATA_HOME" ]]; then
    prefix=~/.local/share
else
    prefix="$XDG_DATA_HOME"
fi

rm $prefix/krunner/dbusplugins/plasma-runner-krha.desktop
rm $prefix/dbus-1/services/org.kde.krha.service
kquitapp5 krunner

