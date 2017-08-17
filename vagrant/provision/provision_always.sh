#!/usr/bin/env bash
echo "Provision always:"

chmod +x /vagrant/project/rs.sh

su - vagrant -c "
pip install --upgrade pip && \
workon vagrant && \
pip install -r /vagrant/project/requirements.txt"
