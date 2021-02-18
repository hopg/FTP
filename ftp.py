import ftputil, os, getpass
from IPython.display import clear_output

def user_message():
    """
    Prints out error messages to the user.
    """
    global message
    if len(message) != 0:
        print(message)
        message = ""

def connect():
    """
    Attempts to establish a connection with the details specified by the user.
    """
    global ftp
    global message
    global connection
    while True:
        clear_output()
        user_message()
        print("Connect to an FTP Server\nEnter 'q' to quit.")
        server = input("Please enter the address of the FTP server you'd like to connect to: ")
        if server.lower() == "q":
            break
            
        print("Note: You can leave the following two inputs blank to login as 'anonymous'.")
        user = input("Please enter in the user name: ")
        if user.lower() == "q":
            break
        elif user.strip() == "":
            user = "anonymous"
            
        password = getpass.getpass("Please enter in the password of the FTP server: ")
        if password.lower() == "q":
            break
        elif password.strip() == "":
            password = "pass"
            
        try:
            ftp = ftputil.FTPHost(server, user, password)
        except:
            message = "Please ensure that your details are correct."
        else:
            message = f"Connection to {server} was successful!\n"
            connection = server
            break

def user_choice(inpt, directory):
    """
    Returns value from the dictionary specified based on the inpt.
    """
    global message
    direct_dict = dict(enumerate(directory, 1))

    try:
        int(inpt)
    except:
        if inpt in direct_dict.values():
            return inpt
        else:
            message = "Please ensure that you have spelled the item name correctly."
    else:
        inpt = int(inpt)
        if inpt in direct_dict.keys():
            return direct_dict[inpt]
        else:
            message = "Please ensure that you have selected a number corresponding to the item."

def enumerate_list(item):
    """
    Displays list of items with an added enumeration.
    """

    for i in range(len(item)):
        item[i] = item[i].rstrip()
        item[i] = item[i].ljust(30)

    for j in range(len(item)):
        if j% 2 == 0:
            print("{0[0]}) {0[1]}".format(tuple(enumerate(item, 1))[j]), end="\t")
        else:
            print("{0[0]:>20}) {0[1]}".format(tuple(enumerate(item, 1))[j]))

def progress(chunk):
    """
    Download progress indicator.
    """
    global total
    total += len(chunk)
    clear_output()
    print(f"Downloading: {(round((int(total)/int(dl_size))*100, 2))}", end="%...")

def file_check(directory):
    """
    Check to determine whether or not a file is selected instead of a directory.
    """
    global message
    try:
        ftp.chdir(directory)
    except:
        message = "Please ensure that you have selected a directory and not a file!"

def folder_check(file_name):
    """
    Check to determine if the user is attempting to download a folder instead of a file.
    """
    global message
    global re_dl
    global dl

    try:
        ftp.download(file_name, os.getcwd() + '\\' + file_name, progress)
    except:
        re_dl = False
        dl = ""
        message = f"You have accidentally selected a directory!"
    else:
        message = "Download complete!"

def change_directory(ftp):
    """
    Changes the current working directory.
    """
    global message
    while True:
        clear_output()
        user_message()
        print("Change Directory")
        print("Type in the name of the directory, enter in the item number, or use 'cd <directory-path>' to change directory.")
        print(f"Enter 'q' to quit.\n\nYou are currently in {ftp.getcwd()}\n")

        enumerate_list(ftp.listdir(ftp.curdir))
        directory_list = (ftp.listdir(ftp.curdir))
        destination = input("\nWhich folder would you like to go to?: ")

        if destination == "q":
            break

        elif destination.strip().lower()[:5] == "cd ..":
            ftp.chdir(ftp.getcwd()[:ftp.getcwd().rindex("/") + 1]) # +1 for case moving to home
            message = f"You have moved directory to {ftp.getcwd()}"

        elif destination.strip().lower()[:3] == "cd ":
            try:
                ftp.chdir(destination[3::])
            except:
                message = "Check that you've entered in the correct directory name!"
                message += "\nIf moving up directories include '/' as a prefix."

        else:
            destination = user_choice(destination, directory_list)
            if message == "":
                file_check(destination)

def ftp_download(ftp, file_name):
    """
    Downloads a file from a FTP server.
    """

    global download
    global message
    global total
    global dl_size
    global re_dl
    global dl

    re_dl = True
    total = 0
    dl_size = ftp.path.getsize(file_name)
    while True:
        clear_output()
        user_message()
        print(f"The file you have selected is {file_name}")
        ans = input(f"The download size is {str(round(dl_size/1024/1024, 2))} mb, would you like to download?: ").lower()

        if len(ans) == 0 or ans[0] not in ('y', 'n', 'q'):
            message = "Please enter in 'y'/'n' or 'q' to quit"

        elif ans[0] == 'q':
            message = "Quitting download..."
            download = False
            break

        else:
            if ans[0] == 'y':
                folder_check(file_name)

                while re_dl:
                    user_message()
                    dl = input("Would you like to download another file?: ").lower()

                    if len(dl) == 0 or dl[0] not in ('y', 'n', 'q'):
                        clear_output()
                        message = "Please enter in 'y'/'n' or 'q' to quit"
                    else:
                        re_dl = False

                else:
                    if len(dl) == 0 or dl[0] == 'y':
                        break  
            
                    else:
                        message = "Quitting download..."
                        download = False
                        break
            else:
                message = f"You did not download the file {file_name}!"
                break

def ftp_download_menu(ftp):
    """
    Provides option for user to download a file within the current directory.
    """
    global file_name
    global download
    global message
    download = True

    while download:
        clear_output()
        user_message()
        print("File Download\nEnter 'q' to quit.\n")
        enumerate_list(ftp.listdir(ftp.getcwd()))
        file_name = input("\nWhat file would you like to download?: ")

        if file_name == 'q':
            download = False
            message = "Quitting download...\n"
            break

        else:
            file_name = user_choice(file_name, ftp.listdir(ftp.getcwd()))

            if message == "":
                try:
                    ftp_download(ftp, file_name)
                except:
                    message = "Please ensure you have spelt the file name correctly."

message = ""
connection = ""
menu_choice = ["Change Directory", "Download File", "Change FTP Server"]
connect()
# Debug server below, comment out connect() and uncomment following lines
# ftp = ftputil.FTPHost('ftp.nluug.nl', 'anonymous', 'pass')
# connection = DEBUG
if len(connection) > 0:
    while True:
        clear_output()
        user_message()
        print(f"Connected to {connection}\nYou are currently in {ftp.getcwd()}\n")
        enumerate_list(menu_choice)
        print("\n\nEnter 'q' to quit from any menu.")
        menu = input("\nWhat would you like to do?: ").lower()

        if menu in ("1", "change directory"):
            change_directory(ftp)
        elif menu in ("2", "download file"):
            download = True
            while download:
                ftp_download_menu(ftp)
        elif menu in ("3", "change ftp server"):
            clear_output()
            connect()
        elif menu == "q":
            print("Closing the connection...")
            ftp.close()
            break
        else:
            message = "Please double check that you've selected something from the menu!"
else:
    print("Quitting program...")
