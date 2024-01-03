# Online Backup Scripts with Mail Notifications

This repository contains the necessary scripts to implement a simple and lightweight online offsite backup with mail notifications.

Within the following quickstart guide the data providing side will be called _backup source_ and the system where the backup should be copied to will be called _backup sink_.

1. Make sure the backup sink has enough space on its disk
2. Create a folder on the backup sink where the backup should be saved e.g. using `mkdir backup`
3. Make sure the backup source and backup sink are within the same network or can reach each other over the internet. When a VPN should be used to connect the two devices, I recommend to use [wireguard](https://www.wireguard.com/)
4. Install openssh-server on the backup sink - on Debian based distros this can be done by typing `sudo apt install openssh-server`
5. Create a [ssh key](https://linux.die.net/man/1/ssh) on the backup source server e.g. using the command `ssh-keygen -t rsa -b 4096`
6. Copy the public key from the backup source to the backup sink e.g. by typing `ssh-copy-id <user on backup sink>@<IP address of backup sink>`
7. Modify the `config.yml` as described in the comments within the `config.yml` file
8. Install the dependencies of the `backup.py` script e.g. by typing `pip install pyyaml` on the backup source system 
9. Execute `python3 backup.py` on the backup source system 

## Setup
This repository contains two folders. The `backup_sink` repository is meant to be used on the system where the backup should be copied to. The `backup_source` repository is meant to be used on the systm which holds the data, which should be backed up.

For the proposed backup scripts it is necessary to ensure that the device which receives the backup has [openssh-server](https://www.openssh.com/) installed and is reachable by the device that holds the data that should be backed up. I recommend to create an [ssh](https://linux.die.net/man/1/ssh) key on the data providing system and coping the public key to the backup receiving system. If the backup source and backup sink are not within the same network, I recommend to use a VPN to bring both devices into the same network - especially if the connection routes through the internet. 

### Backup Source System
The `backup_source` folder contains the `backup.py` script that employs [rsync](https://linux.die.net/man/1/rsync) and can be configured using the parameters in a `config.yml` file. In case of an error, a mail is sent to a configured mail address such that backup failures can be monitored. Additionally, mails can be sent as well, if a backup was successful. The `backup.py` system can be executed by typing

```
python3 backup.py
```
while in the `backup_source` folder.

If the `backup.py` script should be executed on a regular basis, e.g. once per day, e.g. [cron](https://linux.die.net/man/5/crontab) can be used.

#### Requirements
The only dependency, beside [python3](https://www.python.org/downloads/) is that the python3 [pyyaml](https://pypi.org/project/PyYAML/) package has to be installed.

#### Configuration
The needed parameters to fully configure can be found within the `backup_source/config.yml` file. The usage of the listed parameters is further described as comments withing the `backup_source/config.yml` file

### Backup Sink System
For the purpose to facilitate the mounting and unmounting of a LUKS encrypted HDD, two scripts can be found within the `backup_sink` folder. If no encryption is used for the mounted HDD, or there is no external drive at all, the scripts can be neglected.

## Backup System Case
In case, a case for the backup sink is required, in my case for a Raspberry Pi 3B and a Toshiba HDD, a suitable case can be found [here](https://www.thingiverse.com/thing:6412863) which is printable using a 3D printer.

## License
Have a look at the `LICENSE` file for further information.

## Authors
For further questions feel free to open an issue.
