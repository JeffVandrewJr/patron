#!/bin/bash

host=$1
email=$2
key=$(hexdump -n 24 -e '4/4 "%08X"' /dev/urandom)
file="opt-librepatron.custom.yml"

cat opt-librepatron.template.yml > $file

sed -i "s/<host>/$host/g" $file
sed -i "s/<email>/$email/g" $file
sed -i "s/<key>/$key/g" $file
