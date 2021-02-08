# [System.Environment]::SetEnvironmentVariable('INCEPTION_DBUSER','inception','User') 
# [System.Environment]::SetEnvironmentVariable('INCEPTION_DBPASSWORD','nlpcovid','User')
# [System.Environment]::SetEnvironmentVariable('INCEPTION_PORT','8080','User')
# [System.Environment]::SetEnvironmentVariable('msqrootp','mysqlnlp','Process')
# [System.Environment]::SetEnvironmentVariable('INCEPTION_HOME','X:\Code\BioNLP\carl\INCEpTION\srv\inception','Process')

$env:INCEPTION_DBUSER='inception'
$env:INCEPTION_DBPASSWORD='nlpcovid'
$env:INCEPTION_PORT=8080
$env:msqrootp='mysqlnlp'
$env:INCEPTION_HOME='X:\Code\BioNLP\carl\INCEpTION\srv\inception'

#Print
$env:INCEPTION_DBUSER
$env:INCEPTION_DBPASSWORD
$env:INCEPTION_PORT
$env:msqrootp
$env:INCEPTION_HOME


