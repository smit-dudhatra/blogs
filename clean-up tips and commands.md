Full upgrade (recommended):

sudo apt full-upgrade -y

Can remove obsolete packages if needed
Handles dependency changes better

sudo apt autoremove -y
sudo apt autoclean
sudo apt-get clean
rm -rf ~/.cache/thumbnails/*
rm -rf ~/.cache/*

journalctl --disk-usage

check and remove 

/var/log directory
