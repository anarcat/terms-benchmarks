#!/bin/sh

# this is supposed to bootstrap a file to cat on the terminal.
#
# this should be accompanied by another script which cats the created
# file.
head -c "$1" /dev/urandom | base64 > bytes.raw
