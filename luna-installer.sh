#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo "This installer must be run as root."
    echo "Use the command 'sudo su -' (include the trailing hypen) and try again"
    exit 1
fi

(return 2>/dev/null) && sourced=1 || sourced=0

if [ $sourced != 1 ]; then
    echo "You forgot the leading '.' followed by a space!"
    echo "Try this format: . ./luna-installer.sh example.com email@email.com"
    exit 1
fi

if [ -z ${1+x} ]; then
    echo "You forgot to add domain and email!"
    echo "Try again, in this format: ./luna-installer.sh example.com email@email.com"
    exit 1
elif [ -z ${2+x} ]; then
    echo "You forgot to add domain and email!"
    echo "Try again, in this format: ./luna-installer.sh example.com email@email.com"
    exit 1
fi

host=$1
email=$2
file="opt-librepatron.custom.yml"

wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/opt-librepatron.template.yml
cat opt-librepatron.template.yml > $file
rm opt-librepatron.template.yml

sed -i "s/<host>/$host/g" $file
sed -i "s/<email>/$email/g" $file
sed -i "s/<key>/$key/g" $file

mv $file /root/btcpayserver-docker/docker-compose-generator/docker-fragments

if [[ $BTCPAYGEN_ADDITIONAL_FRAGMENTS ==  *"opt-librepatron.custom.yml"* ]]; then
    echo "BTCPAYGEN_ADDITIONAL_FRAGMENTS is already properly set."
elif [ -z ${BTCPAYGEN_ADDITIONAL_FRAGMENTS+x} ]; then
    export BTCPAYGEN_ADDITIONAL_FRAGMENTS="opt-librepatron.custom.yml"
else
    export BTCPAYGEN_ADDITIONAL_FRAGMENTS="${BTCPAYGEN_ADDITIONAL_FRAGMENTS};opt-librepatron.custom.yml"
fi

cd /root/btcpayserver-docker

. ./btcpay-setup.sh -i
