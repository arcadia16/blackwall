#! /bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi
# Project setup
apt-get update -y

if [[ $1 -eq "install-docker" ]]; then
	echo "Installing Docker..."
	apt-get ca-certificates curl

	# Installing docker
	install -m 0755 -d /etc/apt/keyrings
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
	chmod a+r /etc/apt/keyrings/docker.asc
	echo \
	  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
	  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
	  tee /etc/apt/sources.list.d/docker.list > /dev/null
	apt-get update

	sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
	echo "Docker installation was not asked, next."
fi

# Make a wget for server.zip from github??
echo "Prepating bwserver.service..."
mkdir /var/www
cp blackwall_server/deploy/bwserver.service /etc/systemd/system/bwserver.service

echo "Setting up blackwall server..."
chmod +x blackwall_server/start_server.sh
cp blackwall_server/ /var/www/blackwall_server/

echo "Starting server..."
systemctl enable bwserver
systemctl start bwserver