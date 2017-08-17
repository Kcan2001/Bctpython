#!/usr/bin/env bash

echo "Hello, Developer! We will install all packages and dependencies now. GL and have fun!"
echo "Btwn, you can take a cup of tea, we need some time."
echo "Installing system packages"
apt-get update -y
apt-get upgrade -y

# Python2
sudo apt-get -y install git git-core python-dev python-setuptools python-pip libjpeg-dev zlib1g-dev libpng12-dev build-essential libpcre3 libpcre3-dev libpq-dev libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk libxml2-dev libxslt1-dev mc htop vim Xvfb dos2unix
# Python3
sudo apt-get -y install build-essential python3-pip libbz2-dev libncurses5-dev libreadline6-dev libsqlite3-dev libgdbm-dev liblzma-dev tk8.6-dev libssl-dev python3-setuptools python3-dev libffi-dev python3 gconf2

# Dependencies for virtualenv
apt-get install -y libjpeg8 libjpeg8-dev libtiff-dev zlib1g-dev libfreetype6-dev liblcms2-dev libxml2-dev libxslt1-dev libffi-dev libssl-dev swig libyaml-dev libpython2.7-dev

# graphics support for Pillow (jpg, png etc)
apt-get -y build-dep python-imaging
apt-get install -y libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

dos2unix /vagrant/project/rs.sh

echo "Setting up pip and virtualenv for python2"
pip install virtualenv
pip install virtualenvwrapper

echo "Setting up pip and virtualenv for python3"
pip3 install virtualenv
pip3 install virtualenvwrapper

echo "Creating virtualenv and configuring app"
su - vagrant -c "
mkdir -p /home/vagrant/envs && \
export WORKON_HOME=~/envs && \
source /usr/local/bin/virtualenvwrapper.sh && \
mkvirtualenv vagrant -p /usr/bin/python3 && \
pip install -r /vagrant/project/requirements.txt && \
cd /vagrant/project && \
python manage.py migrate --noinput"

cp -p /vagrant/vagrant/templates/.bashrc /home/vagrant/.bashrc
#cp -p /vagrant/vagrant/env.vagrant /vagrant/.env

dos2unix /home/vagrant/.bashrc
