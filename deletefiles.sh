# Run this script for a clean slate
# This file deletes all the video footage that is on the system,
# as well as the database file used for hosting the website. Run
# launcher.sh after executing this script, and a new database
# will be created.
cd /home/pi/Desktop/Security_Cam_Project
sudo rm footage.sqlite
cd /var/www/html/Video_Footage
sudo rm *