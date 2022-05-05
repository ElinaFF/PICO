import os
import pkg_resources
import platform
import subprocess
#import git

REQUIREMENT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'requirement.txt'))

def checkIfMinimumFileRequirementExist():
    print("Checking minimum file requirement...")
    return os.path.exists('matabodashboard') and os.path.exists('requirement.txt')

def installFromGitHub():
    print("installing from git \n")


def installDepencies():
    print("Installing dependencies...")
    return True
    with open(REQUIREMENT_FILE, 'r') as f:
        requirements = f.read().splitlines()
    print("Dependencies not found. Installation is starting...\n")
    os.system("python -m pip install --user -r " + REQUIREMENT_FILE)
    try:
        pkg_resources.require(requirements)
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict) as error:
        print("\nInstallation failed with error:", str(error))
        print("Please install MetaboDashboard dependencies manually.")
        exit()

def checkForDepencies():
    with open(REQUIREMENT_FILE, 'r') as f:
        requirements = f.read().splitlines()
    try:
        pkg_resources.require(requirements)
        return True
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict) as error:
        print(str(error))
        return False

def main():
    osUsed = platform.system()
    versionPython = platform.python_version()

    if not checkIfMinimumFileRequirementExist():
        # TODO : impossible de run avec la commande python3
        print("\033[33m{}\033[00m".format("WARNING : This script is not compatible with the command python3\n"))
        print("MetaboDashboard is starting... \n")

    print("Checking dependencies...")
    if not checkForDepencies():
        installDepencies()

    if checkIfMinimumFileRequirementExist():
        print("Dependencies are OK.\n")
        print("Server is starting...\n")
        from metabodashboard import app
        app.run_server(debug=True, host='127.0.0.1', port=5000)
    else :
        print("Installation Error : Please check the metadashboard folder.")  # TODO : ajouter un message d'erreur


if __name__ == "__main__":
    main()
