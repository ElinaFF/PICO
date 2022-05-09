import os
import pkg_resources
import platform
import subprocess
#import git

REQUIREMENT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'requirement.txt'))
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
MINICONDA_EXEFILE = os.path.abspath(os.path.join(ROOT_DIR, 'Miniconda3-latest.exe'))

def checkIfMinimumFileRequirementExist():
    print("Checking minimum file requirement...")
    return os.path.exists('matabodashboard') and os.path.exists('requirement.txt')


def installFromGitHub():
    print("installing from git \n")


def downloadMiniconda(url_for_download: str):
    request = requests.get(url_for_download)
    with open(MINICONDA_EXEFILE, 'wb') as exeFile:
        exeFile.write(request.content)


def installMinicondaForWindows():
    conda_for_windows = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86{'_64' if is_os_64bit() else ''}.exe"
    downloadMiniconda(conda_for_windows)
    install_conda_command = f"start /wait {MINICONDA_EXEFILE} /InstallationType=JustMe /RegisterPython=0 /S " \
                            f"/AddToPath=1 /D=%UserProfile%\Miniconda3"
    subprocess.check_call(install_conda_command, shell=True)
    subprocess.check_call("set PATH=%PATH%;%UserProfile%\\Miniconda3\\Library\\bin", shell=True)


def installMinicondaForLinux():
    conda_for_linux = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86{'_64' if is_os_64bit() else ''}.sh"
    downloadMiniconda(conda_for_linux)
    install_conda_command = f"bash {MINICONDA_EXEFILE}"
    subprocess.check_call(install_conda_command, shell=True)


def installMinicondaForMacOS():
    conda_for_macos = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86{'_64' if is_os_64bit() else ''}.sh"
    downloadMiniconda(conda_for_macos)
    install_conda_command = f"bash {MINICONDA_EXEFILE}"
    subprocess.check_call(install_conda_command, shell=True)


def is_conda_installed() -> bool:
    try:
        subprocess.check_call("conda env list", shell=True)
    except subprocess.CalledProcessError:
        return False
    return True


def is_metabodashboard_env_exist() -> bool:
    enviList = subprocess.check_output("conda env list", shell=True)
    if "metabodashboard" in enviList.decode('utf-8'):
        return True
    return False


def create_metabodashboard_env():
    subprocess.check_call("conda create -n metabodashboard -f environment.yml", shell=True)


def is_os_64bit():
    return platform.machine().endswith('64')


# TODO : add version verification (useless at first sight)
def env_dependencies_verification():
    # Contient OBLIGATOIREMENT un '=={version}'
    actualPackageInstalledList = subprocess.check_output("pip freeze")
    with open(REQUIREMENT_FILE, 'r') as f:
        line = f.readline()
        while line:
            lineWithoutVersion = line.split('==')[0]
            if lineWithoutVersion not in actualPackageInstalledList.decode('utf-8'):
                print(f"{lineWithoutVersion} couldn't be installed")
                return False
    return True


def main():
    osUsed = platform.system()

    print("Checking for conda installation...")
    if not is_conda_installed():
        print("conda not found !")
        print("Installing MiniConda...")
        if osUsed == "Windows":
            installMinicondaForWindows()
        elif osUsed == "Linux":
            installMinicondaForLinux()
        elif osUsed == "Darwin":
            installMinicondaForMacOS()
        print("Conda installation done.\nPlease restart the launcher")
        exit(0)

    print("\nChecking for metabodashboard environment...")
    if not is_metabodashboard_env_exist():
        print("metabodashboard environment not found !")
        print("Creating metabodashboard environment...")
        create_metabodashboard_env()

    print("\nChecking for source code...")
    if not checkIfMinimumFileRequirementExist():
        print("Source code not found !")
        print("Downloading source code...")
        installFromGitHub()

    subprocess.check_call("conda activate metabodashboard")

    if not env_dependencies_verification():
        raise RuntimeError("Missing package in the conda environment after setup\nTry installing it manually")

    print("Success !")


if __name__ == "__main__":
    main()
