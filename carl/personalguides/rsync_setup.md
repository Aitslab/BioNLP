rsync -aP "/mnt/c/Users/callebalik/OneDrive - Lund University/@Proj/ProjektArbete" /srv/inception/server-data/

rsync -aP "/mnt/c/Users/callebalik/OneDrive - Lund University/@Proj/ProjektArbete" /srv/inception/server-data/

# Sync from homebase
sudo rsync -aP "/mnt/x/OneDrive - Lund University/@Proj/ProjektArbete/backup/" /srv/rsync/backups

#sync on linux
sudo rsync -aP /srv/rsync/backups/

sudo rsync -aP /srv/rsync/backups/SurfaceUb18.04/server-data/ /srv/inception/server-data/   