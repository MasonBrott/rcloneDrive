import os
import subprocess

user = os.environ['USER']

def userDrive():
    backend = [
        "[gdrive]\n",
        "type = drive\n",
        "scope = drive\n"
        "service_account_file = /home/mason/Desktop/cmmcmsp-dev-4a7a4f1eae0a.json\n"
        "impersonate = " + user
    ]

    try:
        with open("/home/mason/.config/rclone/rclone.conf", "w+") as conf:
            conf.writelines(backend)
    except IOError as e:
        print("File can not be opened. Make sure file is not already in use.")
        SystemExit

    with subprocess.Popen(['rclone', 'mount', "gdrive:", '/home/mason/gdrive']) as userMount:
                        print("Drive mounted")


try:
       userDrive()
except KeyboardInterrupt:
       SystemExit