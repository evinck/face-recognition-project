#!/bin/bash

# wait for database to be ready
FILE='/opt/oracle/oradata/.FREE.created'
while true
do
    if [ -e $FILE ]; then
        echo 'DB creation has been completed'
        break
    fi
    echo 'Waiting for DB initialization'
    sleep 5
done

# if jq is not available unfortunately
USERNAME=$(grep -oP '"username"\s*:\s*"\K[^"]+' /home/oracle/config.json)
PASSWORD=$(grep -oP '"password"\s*:\s*"\K[^"]+' /home/oracle/config.json)
# USERNAME=$(jq -r 'database-config.username' config.json)
# PASSWORD=$(jq -r 'database-config.password' config.json)

# Run SQL script with parameters
sqlplus / as sysdba <<EOF
    ALTER SESSION SET CONTAINER = FREEPDB1;
    CREATE USER $USERNAME IDENTIFIED BY $PASSWORD;
    GRANT CONNECT, RESOURCE TO $USERNAME;
    GRANT CREATE SESSION TO $USERNAME;
    GRANT UNLIMITED TABLESPACE TO $USERNAME;

    CONNECT $USERNAME/$PASSWORD@FREEPDB1;
    @/home/oracle/create-tables.sql
    exit;
EOF