#s/^CREATE DATABASE sensors /CREATE DATABASE sensors2 /
/GT-WT02 Temperature=[3-9]/d
/GT-WT02 Temperature=1[0-9][0-9]/d
/GT-WT02 Temperature=-/d
/^sensors,topic=GT-WT02 Humidity=/d
/^devices.*value/d
