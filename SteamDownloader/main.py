import os
import subprocess
import time
from colorama import Fore
import shutil
from pathlib import Path

scriptPath = Path(__file__)
parentPath = scriptPath.parent
steamCMDBinPath = parentPath / "SteamCMDBin"
contentPath = steamCMDBinPath / "steamapps" / "workshop" / "content"
steamCMDPath = steamCMDBinPath / "steamcmd.exe"
addonsPath = parentPath / "Addons"
gameID = 2212330

def installMods(ids:list[int]):
    install_command = []
    for x in ids:
        if type(x) != type(1):
            continue
        if Path(addonsPath / str(x)).exists():
            print(Fore.RED + "You already installed the addon with the id " + str(x))
        else:
            install_command += ["+workshop_download_item " + str(gameID) + " %s"%x]

    print("Installing %s"%str(ids))
    subprocess.call([steamCMDPath, "+@sSteamCmdForcePlatformType windows" ,"+login anonymous"] + install_command + ["+quit"], stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    for x in os.listdir(str(contentPath / str(gameID))):
        shutil.move(str(contentPath / str(gameID) / str(x)), str(addonsPath))

def installModCommand():
    print(Fore.WHITE + "(Make sure to insert the right game ID, the current one is: %s)"%gameID)
    id = input(Fore.GREEN + "Insert the id of the mod you want to download:" + Fore.WHITE)
    if int(id):
        id = int(id)
        pass
    
    installMods([id])

def bulkInstallModsCommand():
    print(Fore.WHITE + "(Make sure to insert the right game ID, the current one is: %s)"%gameID)
    print(Fore.RED + "!SEPARATE EACH MOD ID WITH A SPACE!")

    ids = input(Fore.GREEN + "Insert the id of the mods you want to download:" + Fore.WHITE)
    idsList = []

    for x in ids.split(" "):
        idsList += [int(x)]
    installMods(idsList)

def helpCommand():
    print(Fore.GREEN + "Command list:" + Fore.BLUE)

    for x in commands:
        print(" -" + x)

def setGameId():
    print(Fore.WHITE + "(Make sure to insert the right game ID, the current one is: %s)"%gameID)
    id = input(Fore.GREEN + "Insert the id of the game you want to download addons for (Insert '-' to cancel): " + Fore.WHITE)

    if id == "-":
        print(Fore.RED + "Cancelled setting game id")

    return "GAMEID", id

commands = {
    "set game id": setGameId,
    "install mod" : installModCommand,
    "help" : helpCommand,
    "bulk install mods": bulkInstallModsCommand
}

helpCommand()

while True:
    currentCommand = input(Fore.GREEN + "\nInsert your command: " + Fore.WHITE)
    result = None

    if currentCommand in list(commands.keys()):
        print()
        if currentCommand == "set game id":
            result , id = commands[currentCommand]()
            gameID = id
        else:
            commands[currentCommand]()

    else:
        print(Fore.RED + "Command doesn't exist!")
