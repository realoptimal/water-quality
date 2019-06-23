#!/usr/bin/env bash

# This can be changed for given setup, defaults to brew install location
MY_CNF_LOCATION=/usr/local/etc/my.cnf
MY_ADMIN_USER=root
DB_NAME=water_quality_ng
DB_PASSWD=gobbldeygook

SYSTEM_USER=wqadmin

echo "Setting up database and system user..."

# If /root/.my.cnf exists then it won't ask for root password
if [ -f "${MY_CNF_LOCATION}" ]; then
	echo "Located my.cnf file"
    mysql -u "${MY_ADMIN_USER}" -e "CREATE DATABASE ${DB_NAME} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
    mysql -u "${MY_ADMIN_USER}" -e "CREATE USER ${SYSTEM_USER} IDENTIFIED BY '${DB_PASSWD}';"
    mysql -u "${MY_ADMIN_USER}" -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${SYSTEM_USER}'@'localhost';"
    mysql -u "${MY_ADMIN_USER}" -e "FLUSH PRIVILEGES;"

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
virtualenv -p python3.7 wq_env
source ./wq_env/bin/activate
pip install -r requirements.txt

echo "Done."

