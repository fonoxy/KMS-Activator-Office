import os
import urllib.request
import requests
import time
import glob

# Sets the host and kmshost and calls the get_versions function
def setup(h="http://au.ldtp.com",kh="au.ldtp.com",r="/kms/office"):
    os.system("cls")
    global host, versions, kmshost, root
    host = h
    kmshost = kh
    root = r
    versions = get_versions()
    os.system("cls")
    main_menu()

# Return the selected version name from the list 
def selected_version(number):
    global versions
    return versions[number - 1]

# Gets all the available version it supports
def get_versions():
    response = requests.get(f"{host}{root}/?versions")
    versions = response.json()
    return versions

# Gets the key based on what version is specified by making a web request
def get_key(ver):
    ver = ver.replace(" ", "%20")
    ver = requests.get(f"{host}{root}/?id={ver}")
    return ver.text

# Activates windows to the host kmshost depending on the name of the version.
def activate(selected_version):
    os.system(f'title Activating {selected_version}')
    office_folder = glob.glob("C:\\Program Files\\Microsoft Office\\Office*")[0]
    office_path = os.path.join(office_folder, "ospp.vbs")
    key = get_key(selected_version)
    os.system(f"cscript \"{office_path}\" /inpkey:{key}")
    os.system(f"cscript \"{office_path}\" /sethst:{kmshost}")
    os.system(f"cscript \"{office_path}\" /act")
    print("Exiting in 3 seconds")
    time.sleep(3)
    os.system("exit")

def install(selected_version):
    os.system("cls")
    os.system(f"title Installing {selected_version}")
    print(f"Installing {selected_version}")
    urllib.request.urlretrieve(f"{host}{root}/setup.exe", "setup.exe") # downloads the installer
    urllib.request.urlretrieve(f"{host}{root}/?id={selected_version.replace(" ", "%20")}&xml", "selected_version.xml") # downloads the xml file that contains the correct version to install
    os.system("setup.exe /configure selected_version.xml") # runs the installation script
    os.system("del setup.exe selected_version.xml")
    print(f"{selected_version} installer has finished if there was an error make sure this was run as an Administrator and Office is not installed already.\n \nDo you want to activate Office {selected_version}\nType 'yes' to activate or press Enter (leave blank) to skip.")
    selection = input("Selection: ").lower()
    if selection == "yes":
        os.system("cls")
        activate_menu()
    else:
        print("Exiting in 3 seconds.")
        time.sleep(3)
        os.system("exit")   

# Lets you choose between Installing or Activatinf Windows
def main_menu():
    os.system('title Office Installer and Activator')
    os.system("cls")
    print("Office Installer and Activator\n1. Install Office\n2. Activate Office")
    selection = int(input("Selection : "))
    if selection == 1:
        os.system("cls")
        install_menu()
    elif selection ==2:
        os.system("cls")
        activate_menu()
    elif selection == 3:
        os.system("cls")
        set_host_menu()
    else:
        print("Invalid Option")
        time.sleep(1)
        os.system("cls")
        main_menu()

def install_menu():
    global versions
    os.system("title Office Installer")
    print("Office Installer \nIT WILL NOT WORK IF YOU ALREADY HAVE A OFFICE VERSION INSTALLED!!!")
    for n, i in enumerate(versions):
        print(f"{n+1}. {i}")
    response = int(input("Selection: "))
    if isinstance(response, int) and 1 <= response <= len(versions) :
        selected_option = selected_version(response)
        install(selected_option)
    else: # If the option is not a interger than the respone will be invalid
        print("Invalid Option")
        time.sleep(1)
        os.system("cls")
        install_menu()

# Makes you select which version you want to install based on the available options
def activate_menu():
    global versions
    os.system("title Office Activator")
    print("Office Activator \nPlease make sure your only activating the version you installed")
    for n, i in enumerate(versions): # enumerate adds a number before every version so it can print it with it
        print(f"{n+1}. {i}")
    response = int(input("Selection: "))
    if isinstance(response, int) and 1 <= response <= len(versions) : # makes sure the respone is within the range of the versions currenlty 1-6
        selected_option = selected_version(response)
        activate(selected_option)
    else: # If the option is not a interger than the respone will be invalid
        print("Invalid Option")
        time.sleep(1)
        os.system("cls")
        activate_menu()

# This menu allows you to change the host mainly used if multiple domains to one ip and if kms host every goes offline
def set_host_menu():
    os.system("cls")
    os.system("title Host Setting Screen/Menu")
    h = input("Example of host 'http://example.com' include the http:// or https:// \nSet Host: ")
    kh = input("\nExample of KMS host 'example.com' DO NOT INCLUDE http:// or https:// or any other protocols\n Set KMS Host: ")
    r = input("\n Example of root '/office/kms' Make sure you include the slash at the start but not at the end\n Set Root Path: ")
    setup(h,kh,r)

setup()
