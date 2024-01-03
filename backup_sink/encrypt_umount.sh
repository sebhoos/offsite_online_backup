#!/bin/bash

echo "Unmount backup disk"
umount /media/BackupPiVol

echo "Encrypt disk"
cryptsetup luksClose /dev/sda1 BackupPiVol

echo "Done"
