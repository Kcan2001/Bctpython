export WORKON_HOME=~/envs
source /usr/local/bin/virtualenvwrapper.sh

alias rs="/vagrant/project/rs.sh"
alias test="cd /vagrant/project; python manage.py test --nomigrations"

workon vagrant
cd /vagrant/project/
