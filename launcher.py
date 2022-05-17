import itertools
import os
import platform
import subprocess
import threading
from itertools import cycle
from time import sleep
import logging

try:
    import requests
except ImportError:
    subprocess.call(['pip', 'install', 'requests'])
    import requests

try:
    import argparse
except ImportError:
    subprocess.call(['pip', 'install', 'argparse'])
    import requests

REQUIREMENT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'requirements.txt'))
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
MINICONDA_FILE = os.path.abspath(
    os.path.join(ROOT_DIR, 'Miniconda3-latest'))

RO_TEMP_TOKEN = "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"

parser = argparse.ArgumentParser(description='Installation parameter')
parser.add_argument('-e', '--environment', help='Conda environment name')
condaEnvName = parser.parse_args()
logging.basicConfig(level=logging.INFO, filename='MetabodashboardInstallation.log', filemode='w', format='%(asctime)s - %(levelname)s - %(funcName)s (ligne %(lineno)d) - %(message)s')

class Loader:
    def __init__(self, desc="Loading...", end="checked", fail="fail",
                 timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            fail (str, optional): Fail print. Defaults to "❌".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.fail = fail
        self.timeout = timeout

        self._thread = threading.Thread(target=self._animate, daemon=True)
        self.steps = ["|MetaboDashboard   |", "| MetaboDashboard  |", "|  MetaboDashboard |", "|   MetaboDashboard|",
                      "|    MetaboDashboar|", "|d    MetaboDashboa|", "|rd    MetaboDashbo|", "|ard    MetaboDashb|",
                      "|oard    MetaboDash|", "|board    MetaboDas|", "|hboard    MetaboDa|", "|shboard    MetaboD|",
                      "|ashboard    Metabo|", "|Dashboard    Metab|", "|oDashboard    Meta|", "|boDashboard    Met|",
                      "|aboDashboard    Me|", "|taboDashboard    M|", "|etaboDashboard    |"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}          ", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self, fail=False):
        self.done = True
        print(f"\r{self.desc}       {self.end if not fail else self.fail}                               ",
              flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


def checkIfMinimumFileRequirementExist():
    logging.info("Checking if the github repository is already downloaded")
    return os.path.exists('metabodashboard') and os.path.exists(
        'requirements.txt')


def installFromGitHubForWindows():
    # TODO : mettre repo en public
    logging.info("Downloading project file from github")
    subprocess.call("rmdir /s /q cloneForInstallation", shell=True, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
    subprocess.call("git clone -b cloneForInstallation "
                    f"https://{RO_TEMP_TOKEN + '@'}github.com/ElinaFF/MetaboDashboard cloneForInstallation",
                    shell=True, stdout=subprocess.DEVNULL)
    subprocess.call("robocopy /s cloneForInstallation .", shell=True)
    subprocess.call("rmdir /q /s cloneForInstallation", shell=True)


def installFromGitHubForLinux():
    logging.info("Downloading project file from github")
    subprocess.call("rm -rf MetaboDashboard", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.check_call("git clone -b cloneForInstallation "
                          f"https://{RO_TEMP_TOKEN + '@'}github.com/ElinaFF/MetaboDashboard",
                          shell=True, stdout=subprocess.DEVNULL)
    subprocess.check_call("mv MetaboDashboard/* ../", shell=True)
    subprocess.check_call("rm -r MetaboDashboard", shell=True)


def downloadMiniconda(url_for_download: str, extension: str = ".sh"):
    logging.info("Downloading MiniConda")
    request = requests.get(url_for_download)
    with open(MINICONDA_FILE + extension, 'wb') as exeFile:
        exeFile.write(request.content)


def installMinicondaForWindows():
    conda_for_windows = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86{'_64' if is_os_64bit() else ''}.exe"
    downloadMiniconda(conda_for_windows, extension=".exe")
    logging.info("Installing MiniConda for Windows")
    install_conda_command = f"start /wait {MINICONDA_FILE + '.exe'} /InstallationType=JustMe /RegisterPython=0 /S " \
                            f"/AddToPath=1 /D=%UserProfile%\Miniconda3"
    subprocess.check_call(install_conda_command, shell=True,
                          stdout=subprocess.DEVNULL)
    subprocess.check_call(
        "SET PATH=%PATH%;%UserProfile%\\Miniconda3\\Library\\bin", shell=True,
        stdout=subprocess.DEVNULL)


def installMinicondaForLinux():
    conda_for_linux = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86{'_64' if is_os_64bit() else ''}.sh"
    downloadMiniconda(conda_for_linux)
    logging.info("Installing MiniConda for Linux")
    install_conda_command = f"bash {MINICONDA_FILE + '.sh'}"
    subprocess.check_call(install_conda_command, shell=True)


def installMinicondaForMacOS():
    conda_for_macos = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86{'_64' if is_os_64bit() else ''}.sh"
    downloadMiniconda(conda_for_macos)
    logging.info("Installing MiniConda for MacOs")
    install_conda_command = f"bash {MINICONDA_FILE + '.sh'}"
    subprocess.check_call(install_conda_command, shell=True)


def is_conda_installed() -> bool:
    logging.info("Checking for conda installation")
    try:
        subprocess.check_call("conda env list", shell=True,
                              stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        logging.info("Cannot find conda")
        return False
    logging.info("Conda found")
    return True


def is_metabodashboard_env_exist() -> bool:
    logging.info(f"Checking for {condaEnvName.environment} conda environment")
    enviList = subprocess.check_output("conda env list", shell=True)
    if "\n" + condaEnvName.environment + " " in enviList.decode('utf-8').lower():
        logging.info(f"{condaEnvName.environment} conda environment found")
        return True
    logging.info(f"{condaEnvName.environment} conda environment not found")
    return False


def create_metabodashboard_env():
    logging.info("metadashboard conda environment creation")
    subprocess.check_call("conda create -n metabodashboard -y python=3.8", shell=True,
                          stdout=subprocess.DEVNULL)


def install_dependencies():
    logging.info(f"Installation of the dependencies in {condaEnvName.environment} conda environment")
    subprocess.check_call(
        "conda run -n " + condaEnvName.environment + " pip install -r requirements.txt --user", shell=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def is_os_64bit():
    return platform.machine().endswith('64')


# TODO : add version verification (useless at first sight)
def env_dependencies_verification():
    logging.info(f"Verification of the dependencies in {condaEnvName.environment} conda environment")
    # Contient OBLIGATOIREMENT un '=={version}'
    actualPackageInstalledList = subprocess.check_output(
        f"conda run -n {condaEnvName.environment}", shell=True).decode('utf-8')
    with open(REQUIREMENT_FILE, 'r') as f:
        line = f.readline()
        while line:
            lineWithoutVersion = line.split('==')[0].strip()
            if lineWithoutVersion not in actualPackageInstalledList:
                logging.info(f"{lineWithoutVersion} dependency isn't installed")
                return False
            line = f.readline()
    logging.info("All dependencies are installed")
    return True


def launch_metabodashboard():
    subprocess.check_call(
        "conda run -n " + condaEnvName.environment + " python main.py", shell=True,
        stdout=subprocess.DEVNULL)


def condaHandler():
    osUsed = platform.system()
    loader = Loader(desc="Checking for conda installation...").start()
    if not is_conda_installed():
        loader.stop(fail=True)
        print("conda not found !")
        with Loader(desc="Installing conda..."):
            if osUsed == "Windows":
                installMinicondaForWindows()
            elif osUsed == "Linux":
                installMinicondaForLinux()
            elif osUsed == "Darwin":
                installMinicondaForMacOS()
        print("\nPlease restart the launcher")
        exit(0)
    loader.stop()


def codeSourceHandler():
    osUsed = platform.system()
    loader = Loader(desc="Checking for source code...").start()
    if not checkIfMinimumFileRequirementExist():
        loader.stop(fail=True)
        print("Source code not found !")
        with Loader(desc="\tDownloading source code..."):
            if osUsed == "Windows":
                installFromGitHubForWindows()
            elif osUsed == "Linux" or osUsed == "Darwin":
                installFromGitHubForLinux()

        internal_loader = Loader(
            desc="\tRe-checking for source code...").start()
        if not checkIfMinimumFileRequirementExist():
            internal_loader.stop(fail=True)
            raise Exception("Source code couldn't be downloaded")
        internal_loader.stop()
    loader.stop()


def createMetabodashboardCondaEnv():
    condaEnvName.environment = "metabodashboard"
    loader = Loader(desc="Checking for metabodashboard environment...").start()
    print(is_metabodashboard_env_exist)
    if not is_metabodashboard_env_exist():
        loader.stop(fail=True)
        print("metabodashboard environment not found !")
        with Loader(desc="\tCreating metabodashboard environment..."):
            create_metabodashboard_env()
        with Loader(desc="\tInstalling dependencies in environment..."):
            try:
                install_dependencies()
            except:
                logging.error(
                    f"Installation of the dependencies in {condaEnvName.environment} conda environment failed")
                exit(0)

        internal_loader = Loader(
            desc="Re-checking for metabodashboard environment...").start()
        if not is_metabodashboard_env_exist():
            internal_loader.stop(fail=True)
            logging.error("metabodashboard environment couldn't be created")
            raise Exception("metabodashboard environment couldn't be created")
        internal_loader.stop()
    loader.stop()


def checkOtherEnv():
    loader = Loader(desc=f"Checking for {condaEnvName.environment} environment...").start()
    if not is_metabodashboard_env_exist():
        loader.stop(fail=True)
        print(f"Error : environment {condaEnvName.environment} not found")
        exit(0)
    loader.stop()


def dependencyHandler():
    loader = Loader(desc="Checking dependencies...").start()
    if not env_dependencies_verification():
        loader.stop(fail=True)
        with Loader(desc="\tInstalling dependencies in environment..."):
            try:
                install_dependencies()
            except:
                logging.error(
                    f"Installation of the dependencies in {condaEnvName.environment} conda environment failed")
                exit(0)

        internal_loader = Loader(
            desc="\tRe-checking dependencies...").start()
        if not env_dependencies_verification():
            internal_loader.stop(fail=True)
            raise Exception("Dependencies couldn't be installed")
        internal_loader.stop()
    loader.stop()


def checkPythonVersion():
    loader = Loader(desc=f"Checking of the python version installed...").start()
    pythonVersion = subprocess.check_output(f"conda run -n {condaEnvName.environment} python --version", shell=True).decode('utf-8')
    if "3.8" in pythonVersion:
        logging.info("The correct version of python (3.8) is installed")
        loader.stop()
    else:
        logging.error("Wrong version of python installed, please install python 3.8")
        print("Wrong version of python installed, please install python 3.8")
        loader.stop(fail=True)
        exit(0)


def main():

    condaHandler()

    codeSourceHandler()

    if not condaEnvName.environment:
        createMetabodashboardCondaEnv()
    else:
        checkOtherEnv()
    checkPythonVersion()

    dependencyHandler()

    logging.info("Successfully installed !")
    print("Successfully installed !\n")

    with Loader(desc="Metabodashboard Runing at http://127.0.0.1:5000..."):
        launch_metabodashboard()


if __name__ == "__main__":
    main()
