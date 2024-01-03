#!/bin/bash

echo "Decrypting USB backup drive"
cryptsetup luksOpen /dev/sda1 BackupPiVol

echo "Mounting USB backup drive"
mount /dev/mapper/BackupPiVol /media/BackupPiVol

echo "Done"
