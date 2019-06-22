#!/usr/bin/env bash

# This can be changed for given setup, defaults to brew install location
MYSQL_INSTALL=/usr/local/var/mysql

DB_NAME=water_quality
DB_PASSWD=gobbldeygook

SYSTEM_USER=wqadmin

echo "Setting up database and system user..."

# If /root/.my.cnf exists then it won't ask for root password
if [ -f "${MYSQL_INSTALL}/my.cnf" ]; then

    mysql -e "CREATE DATABASE ${DB_NAME} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
    mysql -e "CREATE USER ${SYSTEM_USER}@localhost IDENTIFIED BY '${DB_PASSWD}';"
    mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${SYSTEM_USER}'@'localhost';"
    mysql -e "FLUSH PRIVILEGES;"

# If /root/.my.cnf doesn't exist then it'll ask for root password   
else
    echo "Please enter root user MySQL password!"
    read -sp rootpasswd
    mysql -uroot -p${rootpasswd} -e "CREATE DATABASE ${DB_NAME} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
    mysql -uroot -p${rootpasswd} -e "CREATE USER ${SYSTEM_USER}@localhost IDENTIFIED BY '${DB_PASSWD}';"
    mysql -uroot -p${rootpasswd} -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${SYSTEM_USER}'@'localhost';"
    mysql -uroot -p${rootpasswd} -e "FLUSH PRIVILEGES;"
fi

echo "Setting up python virtual environment and installing requirements..."
mkvirtualenv -p python3.7 py37-waterquality
pip install -r requirements.txt

echo "Done."

