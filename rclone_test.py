import os
import subprocess
from getpass import getuser
from multiprocessing import Process

# Get the local user account (kasm_user) for paths
localuser = getuser()
# Get the user to impersonate from the user environment variable
user = os.environ['USER']

# Set up the directory to mount the User Gdrive to 
userDirectory = "G"
UserParentDir = "/home/" + localuser
userPath = os.path.join(UserParentDir, userDirectory)
try:
    os.mkdir(userPath)
except FileExistsError:
        pass

shareDirectory = "Gshare"
shareParentDir = "/home/" + localuser
sharePath = os.path.join(shareParentDir, shareDirectory)
try:
    os.mkdir(sharePath)
except FileExistsError:
        pass

def userDrive():
    global userPath
    # Contents of Rclone config file
    backend = [
        "[gdrive]\n",
        "type = drive\n",
        "scope = drive\n"
        "service_account_file = /home/mason/Desktop/cmmcmsp-dev-4a7a4f1eae0a.json\n"
        "impersonate = " + user + "\n",
        "\n",
    ]

    # Write over the contents of the config to contain ours instead
    try:
        with open("/home/" + localuser + "/.config/rclone/rclone.conf", "w+") as conf:
            conf.writelines(backend)
    except IOError as e:
        print("File can not be opened. Make sure file is not already in use.")
        SystemExit

    # Mount Gdrive to the filesystem
    with subprocess.Popen(['rclone', 'mount', "gdrive:", userPath]):
                        pass

def teamDrive():
    global sharePath
    backend = [
    "[share test]\n",
    "type = drive\n",
    "scope = drive\n"
    "service_account_file = /home/mason/Desktop/cmmcmsp-dev-4a7a4f1eae0a.json\n"
    "impersonate = " + user + "\n",
    "team_drive = 0AJb_BTvpKdxFUk9PVA\n",
    "root_folder_id = ",
    "\n",
    ]

    try:
        with open("/home/" + localuser + "/.config/rclone/rclone.conf", "a") as conf:
            conf.writelines(backend)
    except IOError as e:
        print("File can not be opened. Make sure file is not already in use.")
        SystemExit

    # Mount Gdrive to the filesystem
    with subprocess.Popen(['rclone', 'mount', "share test:", sharePath]):
                        pass

if __name__=='__main__':
    p1 = Process(target=userDrive)
    try:
        p1.start()
    except KeyboardInterrupt:
           subprocess.Popen(['fusermount', '-uz', userPath])
           pass
    p2 = Process(target=teamDrive)
    try:
        p2.start()
    except KeyboardInterrupt:
          subprocess.Popen(['fusermount', '-uz', sharePath])
          SystemExit
