#!/bin/bash

export INCEPTION_DBUSER='inception'
export INCEPTION_DBPASSWORD='nlpcovid'
export INCEPTION_PORT=8080
export msqrootp='mysqlnlp'
export INCEPTION_HOME=/srv/inception

# export DBUSER=inception
# export DBPASSWORD=nlpcovid
# export INCEPTION_HOME=/srv/inception
# export INCEPTION_PORT=8080

export DBUSER=inception
export DBPASSWORD=nlpcovid
export INCEPTION_HOME=/srv/inception
export INCEPTION_PORT=8080
docker-compose -p inception up -d