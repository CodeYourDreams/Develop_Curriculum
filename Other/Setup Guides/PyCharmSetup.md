# Pycharm Setup Guide

## Downloading 
### Pycharm Community Edition
1. Go to https://www.jetbrains.com/pycharm/download/
2. Ensure that the correct operating system is selected (Windows, macOS, Linux)
3. Click download in the community edition
### The Latest Version of Python
1. You will also need to download the latest version of python (3.9.6 as of the writing of this) to run your projects. 
2. If you have Windows, click [here](https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe) to download python for your computer
3. If you have macOS, click [here](https://www.python.org/ftp/python/3.9.6/python-3.9.6-macosx10.9.pkg) to download python for your computer
4. If neither of those links work for you, you can manually download the packages you need from https://www.python.org/downloads/release/python-396/


## Installing
### PyCharm
1. Once PyCharm has successfully downloaded, navigate to your downloads folder
2. Click on the Application called something like `pycharm-community-2021.1.3.exe`
3. Click next on the installer until you see the `install` button
4. Click install
5. Once installation is complete, click `Run PyCharm Community Edition` and finish in the bottom right hand corner

### Python
1. Once Python has successfully downloaded, navigate to your downloads folder
2. Click on the Application called `python-3.9.6-amd64.exe` if you have Windows or `python-3.9.6-macosx10.9.pkg` if you have macOS
3. Click `Add to path` at the bottom and then `Install now`

## Setting Up PyCharm
1. Once the application runs, you should be presented with a window titled "Import PyCharm Settings". Click `Do Not Import Settings`
2. When the "Welcome to PyCharm" window appears, click `New Project`
3. For the location, leave it as the default location. 
4. If not automatically selected, you want to create a new environment using `Virtualenv`
5. Leave the default location for the virtualenv
6. The base interpreter should default to where you installed your python package to. If not, navigate to where it installed to select it using the dropdown
7. Select `Inherit global site-packages` and `Make available to all project`
8. Select `Create a main.py welcome script`
9. Finally select `Create` at the bottom right
10. To test that everything is successfully installed, click the green arrow on the top right in between the dropdown that says "main" and the green bug.
11. The code should run and you should see in the bottom console the result `Hi, Pycharm`
