# INCEpTION guidelines for NLP project

## INCEpTION Setup

### Docker-compose 
Setup can be done via a two docker containers. This provies very good cross platform compatability and minimal fuzz


```powershell
.\variables.ps1
# First run the script to add the environment variables to the session while inside the INCEpTION dir of the github repository. 
docker-compose -p inception up -d
# Create Docker containers
```
## Backups

### Gazetters 
It is possible to pre-load gazeteers into string matching recommenders. A gazeteer is a simple text file where each line consists of a text and a label separated by a tab character. The order of items in the gazeteer does not matter. Suggestions are generated considering the longest match. Comment lines start with a #. Empty lines are ignored.

Format schema 
string1 TAG1
string2 TAG2

docker exec inception_mysql sh -c 'exec mysqldump -u inception -p > "X:\OneDrive - Lund University\@Proj\ProjektArbete\INCEPTION_HOMEBASE\DB_backup.sql"'

$ docker exec some-mysql sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > /some/path/on/your/host/all-databases.sql

mysqldump -u root -p database_name > database_name.sql


docker exec inception_mysql sh -c 'exec mysqldump -u inception -p > "/mnt/x/OneDrive - Lund University/@Proj/ProjektArbete/INCEPTION_HOMEBASE/DB_backup.sql"'