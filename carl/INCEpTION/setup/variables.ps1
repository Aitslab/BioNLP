# [System.Environment]::SetEnvironmentVariable('INCEPTION_DBUSER','inception','User') 
# [System.Environment]::SetEnvironmentVariable('INCEPTION_DBPASSWORD','nlpcovid','User')
# [System.Environment]::SetEnvironmentVariable('INCEPTION_PORT','8080','User')
# [System.Environment]::SetEnvironmentVariable('msqrootp','mysqlnlp','Process')
# [System.Environment]::SetEnvironmentVariable('INCEPTION_HOME','X:\Code\BioNLP\carl\INCEpTION\srv\inception','Process')

# $env:msqrootp='mysqlnlp'



$env:DBUSER='inception'
$env:DBPASSWORD='nlpcovid'
$env:INCEPTION_PORT=31415
$env:INCEPTION_HOME='/srv/inception'

#Print
$env:INCEPTION_DBUSER
$env:INCEPTION_DBPASSWORD
$env:INCEPTION_PORT
$env:msqrootp
$env:INCEPTION_HOME


