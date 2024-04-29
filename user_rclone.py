import os
import subprocess
from getpass import getuser

# Get the local user account (kasm_user) for paths
localuser = getuser()
# Get the user to impersonate from the user environment variable
user = os.environ['KASM_USER']

print(localuser)
print(user)

# Set up the directory to mount the User Gdrive to 
userDirectory = "G"
UserParentDir = "/home/" + localuser
userPath = os.path.join(UserParentDir, userDirectory)
try:
    os.mkdir(userPath)
except FileExistsError:
        print("user path file not found")
        pass

def userDrive():
    global userPath
    # Contents of Rclone config file
    backend = [
        "[gdrive]\n",
        "type = drive\n",
        "scope = drive\n"
        "service_account_file = /dockerstartup/cmmcmsp-dev-4a7a4f1eae0a.json\n"
        "impersonate = " + user + "\n",
        "\n",
    ]

    # Write over the contents of the config to contain ours instead
    try:
        with open("/home/" + localuser + "/.config/rclone/rclone.conf", "w+") as conf:
            conf.writelines(backend)
    except IOError as e:
        print("Error writing config")
        pass

    # Mount Gdrive to the filesystem
    with subprocess.Popen(['rclone', 'mount', "gdrive:", userPath]):
                        print("Mounted drive")
                        pass
    

userDrive()
