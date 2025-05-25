#! /bin/bash

while getopts h: flag
do
	case "${flag}" in
		h) host=${OPTARG};;
	esac
done

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

if [ "$#" -eq 0 ]; then
    echo "Pass -h <master ip>"
	exit 1
fi
# Make a wget for agent.zip from github??
echo "Setting up blackwall agent, master server set at $host";

# Project setup
echo "MASTER_SERVER_IP = \"$host\"" >> agent/config.py
apt-get update -y
apt-get install python3 python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

echo "Prepating bwagentice..."
mkdir /var/www
cp blackwall_agent/deploy/bwagent.service /etc/systemd/system/bwagent.service
chmod +x blackwall_agent/start_agent.sh
cp blackwall_agent/ /var/www/blackwall_agent/
echo "Starting server..."
systemctl enable bwserver
systemctl start bwserver