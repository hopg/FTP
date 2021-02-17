# FTP
Program to browse FTP servers with additional functionality. 

## Table of Contents

- [Introduction](https://github.com/hopg/FTP#Introduction)
- [Program](https://github.com/hopg/FTP#Program)
- [Features](https://github.com/hopg/FTP#Features)
- [Required Modules](https://github.com/hopg/FTP#Required-Modules)
- [Known Issues](https://github.com/hopg/FTP#Known-Issues)

## Introduction

File transfer protocol is a network protocol allowing a client to transfer files to and from a server via a network. 

This program establishes a connection to an FTP server, specified by the user, and allows navigation and downloading of files within the server.

## Program
#### Log in

The user will be first prompted to enter in the details of the FTP server they would like to connect to. This requires the following information:
- FTP server
- Username
- Password

If attempting to connect to a public server, or a server that does not require a specific username password combination, the user can login with the default "anonymous" username and associated password of "pass" by simply leaving these two fields left blank and pressing enter. 

#### Menu 

After a successful connection is made, the user is presented with a menu where they can select different options. The options contained in the menu are:
- Change Directory
- Download File
- Change FTP Server

To access any of these options, the user can enter in either the name of the option or the number corresponding to the menu option. To leave the menu and close the FTP connection, `q` can be entered to quit. 

Entering `q` within the menu options will allow a user to quit back to the main menu. 

#### Change Directory

Upon selecting this option, the user will be presented with the directory listing of the current directory. By default, the current directory will be the root and be represented as `/`.
The user can do either one of the following to enter directories:
- Type the name of the directory they would like to navigate into
- Enter in the number corresponding to the directory
- Utilise the `cd` command to navigate through various directory levels

If the user is to accidentally select a file to navigate into, the program will notify the user and ask the user to specify a choice again.

#### Download File

This option will ask the user which file they would like to download within the current directory. The file will be downloaded to the current local directory, that is, where the program was executed. 

The user can either enter in the name of the file they would like to download or they can enter in the associated number to the file. In the scenario where a folder is selected instead of a file, the program will notify the user and prompt the user to select again.

If the file of interest is within a different directory, please use the `Change Directory` option first before selecting this option.

#### Change FTP Server

This option allows the user to close the connection to the current FTP server and specify a different FTP server to connect to. 

### Features
- Options presented in two columns with enumeration
- Program accepts either name of the option or corresponding number as acceptable inputs
- Ability to use `cd` command within `Change Directory` menu option. 
- Within `Change Directory` error handling for selecting a file instead of a directory
- Download size presented to user before confirming download
- Download progress for files as a percentage
- Within `Download` error handling for selecting a directory instead of a file
- `user_message` function which prints out error messages to the user
- `q` to quit from menu options

### Required Modules
- `ftputil`
- `getpass`
- `os`
- `IPthon.display`

### Known Issues
- Unable to quit when entering the details of the FTP server, can lead to be stuck in a loop if valid FTP server details are not entered
- An error is thrown if connection to the server has a timeout after a period of inactivity with the server
- As of current, can only download to the current working directory
