#!/bin/python3

# import section
import yaml
import subprocess
import smtplib
import ssl
from email.message import EmailMessage
import socket
import time
import os

# global members
config = None


def main():
    global config

    error_msg = ""
    error_tracked = False
    start_time = time.time()

    # load config
    with open(os.path.dirname(__file__) + "/config.yml", 'r') as file:
        config = yaml.safe_load(file)

    # check if backup is available
    result = subprocess.run(["ping -c 1 " + config["backup_sink"]["host"]], shell=True, capture_output=True)
    if result.returncode != 0:
        error_tracked = True
        error_msg += "Could not ping backup machine with ip address: " \
                     + config["backup_sink"]["host"] \
                     + ": " + str(result.stdout) + "\n\n"

    # check if backup disk is mounted
    result = subprocess.run(["ssh " + config["backup_sink"]["user"] + "@"
                             + config["backup_sink"]["host"] + " ls " + str(config["backup_sink"]["backup_folder"])],
                            shell=True, capture_output=True)
    if result.returncode != 0:
        error_tracked = True
        error_msg += "Could not execute ls on backup machine with ip address: " \
                     + config["backup_sink"]["host"] \
                     + ": " + str(result.stdout) + "\n\n"
    if str(config["backup_sink"]["is_mounted_indicator"]) not in str(result.stdout):
        error_tracked = True
        error_msg += "Could not find is_mounted_indicator on disk. " \
                     + "Instead the following files and folders were found: " \
                     + str(result.stdout) + "\n\n"

    if not error_tracked:
        # sync folders to backup server
        for folder in config["files"]["folder"]:
            if type(folder) == str:
                command = ["rsync"]
                command.extend(config["files"]["rsync_options"])
                for exclude in config["files"]["exclude"]:
                    command.append("--exclude")
                    command.append(exclude)
                command.extend([config["files"]["prefix_path"] + folder,
                                         "" + str(config["backup_sink"]["user"]) + "@"
                                         + str(config["backup_sink"]["host"]) + ":"
                                         + str(config["backup_sink"]["backup_folder"])])
                result = subprocess.run(command, capture_output=True)
                if result.returncode != 0:
                    error_tracked = True
                    error_msg += "rsync failed with stdout: " + str(result.stdout) + "\n" + "and with stderr: " + str(result.stderr) + "\n\n"
            else:
                error_tracked = True
                error_msg += "One of the given folder names was not a string. Folder object: " + str(folder) + "\n\n"

    # send mail notifications
    if error_tracked:
        send_log_via_mail(error_msg)

    if config["send_mail_after_successful_backup"] and not error_tracked:
        success_msg = "The backup from source " + str(socket.gethostname()) + " to IP adress " + str(config["backup_sink"]["host"]) + " of the folders:\n"
        for folder in config["files"]["folder"]:
            success_msg += str(folder) + "\n"
        success_msg += "has been successful!\nTime needed for backup: " + str(time.time() - start_time) + "\n"
        send_log_via_mail(success_msg)


def send_log_via_mail(message: str = ""):
    global config

    smtp_server = config["mail"]["server"]
    port = config["mail"]["port"]
    sender_email = config["mail"]["account"]
    receiver_email = config["mail"]["receiver"]
    password = config["mail"]["password"]

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            mail_msg = EmailMessage()
            mail_msg["Subject"] = "ONLINE OFFSITE BACKUP NOTICE"
            mail_msg["To"] = receiver_email
            mail_msg["From"] = sender_email
            mail_msg.set_content(message)
            server.send_message(mail_msg)
            server.quit()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
