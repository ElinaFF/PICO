# -*- coding: utf-8 -*-
import itertools
import os
import platform
import re
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

CONDA_PATH = "conda"

RO_TEMP_TOKEN = "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"

parser = argparse.ArgumentParser(description='Installation parameter')
parser.add_argument('-e', '--environment', help='Conda environment name')
conda_env_name = parser.parse_args()
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


def check_if_minimum_file_requirement_exist():
    logging.info("Checking if the github repository is already downloaded")
    return os.path.exists('metabodashboard') and os.path.exists(
        'requirements.txt')


def install_from_git_hub_for_windows():
    # TODO : mettre repo en public
    logging.info("Downloading project file from github")
    subprocess.call("rmdir /s /q cloneForInstallation", shell=True, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
    subprocess.call("git clone -b cloneForInstallation "
                    f"https://{RO_TEMP_TOKEN + '@'}github.com/ElinaFF/MetaboDashboard cloneForInstallation",
                    shell=True, stdout=subprocess.DEVNULL)
    subprocess.call("robocopy /s cloneForInstallation .", shell=True)
    subprocess.call("rmdir /q /s cloneForInstallation", shell=True)


def install_from_git_hub_for_linux():
    logging.info("Downloading project file from github")
    subprocess.call("rm -rf MetaboDashboard", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.check_call("git clone -b cloneForInstallation "
                          f"https://{RO_TEMP_TOKEN + '@'}github.com/ElinaFF/MetaboDashboard",
                          shell=True, stdout=subprocess.DEVNULL)
    subprocess.check_call("mv MetaboDashboard/* ../", shell=True)
    subprocess.check_call("rm -r MetaboDashboard", shell=True)


def download_miniconda(url_for_download: str, extension: str = ".sh"):
    logging.info("Downloading MiniConda")
    request = requests.get(url_for_download)
    with open(MINICONDA_FILE + extension, 'wb') as exe_file:
        exe_file.write(request.content)


def install_miniconda_for_windows():
    conda_for_windows = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86{'_64' if is_os_64bit() else ''}.exe"
    download_miniconda(conda_for_windows, extension=".exe")
    logging.info("Installing MiniConda for Windows")
    install_conda_command = f"start /wait {MINICONDA_FILE + '.exe'} /InstallationType=JustMe /RegisterPython=0 /S " \
                            f"/AddToPath=1 /D=%UserProfile%\Miniconda3"
    subprocess.check_call(install_conda_command, shell=True,
                          stdout=subprocess.DEVNULL)
    subprocess.check_call("SET PATH=%PATH%;%UserProfile%\\Miniconda3\\Library\\bin", shell=True,
        stdout=subprocess.DEVNULL)
    global CONDA_PATH
    CONDA_PATH="%UserProfile%\\Miniconda3\\Library\\bin\\conda"


def install_miniconda_for_linux():
    conda_for_linux = f"https:F//repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86{'_64' if is_os_64bit() else ''}.sh"
    download_miniconda(conda_for_linux)
    logging.info("Installing MiniConda for Linux")
    install_conda_command = f"bash {MINICONDA_FILE + '.sh -b -p ~/miniconda3'}"
    subprocess.check_call(install_conda_command, shell=True)
    subprocess.check_call("export PATH='~/miniconda3/bin:$PATH'", shell=True, stdout=subprocess.DEVNULL)
    global CONDA_PATH
    CONDA_PATH="~/miniconda3/bin/conda"


def install_miniconda_for_mac_os():
    conda_for_macos = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86{'_64' if is_os_64bit() else ''}.sh"
    download_miniconda(conda_for_macos)
    logging.info("Installing MiniConda for MacOs")
    install_conda_command = f"bash {MINICONDA_FILE + '.sh'}"
    subprocess.check_call(install_conda_command, shell=True)
    subprocess.check_call("export PATH='~/miniconda3/bin:$PATH'", shell=True, stdout=subprocess.DEVNULL)
    global CONDA_PATH
    CONDA_PATH = "~/miniconda3/bin/conda"


def is_conda_installed() -> bool:
    logging.info("Checking for conda installation")
    try:
        subprocess.check_call(f"{CONDA_PATH} env list", shell=True,
                              stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        logging.info("Cannot find conda")
        return False
    logging.info("Conda found")
    return True


def is_metabodashboard_env_exist() -> bool:
    logging.info(f"Checking for {conda_env_name.environment} conda environment")
    enviList = subprocess.check_output(f"{CONDA_PATH} env list", shell=True)
    if "\n" + conda_env_name.environment + " " in enviList.decode('utf-8').lower():
        logging.info(f"{conda_env_name.environment} conda environment found")
        return True
    logging.info(f"{conda_env_name.environment} conda environment not found")
    return False


def create_metabodashboard_env():
    logging.info("metadashboard conda environment creation")
    subprocess.check_call(f"{CONDA_PATH} create -n metabodashboard -y python=3.8", shell=True,
                          stdout=subprocess.DEVNULL)


def install_dependencies():
    logging.info(f"Installation of the dependencies in {conda_env_name.environment} conda environment")
    subprocess.check_call(
        f"{CONDA_PATH} run -n " + conda_env_name.environment + " pip install numpy", shell=True,
        stdout=subprocess.DEVNULL)
    subprocess.check_call(
        f"{CONDA_PATH} run -n " + conda_env_name.environment + " pip install -r requirements.txt --user", shell=True,
        stdout=subprocess.DEVNULL)


def is_os_64bit():
    return platform.machine().endswith('64')


# TODO : add version verification (useless at first sight)
def env_dependencies_verification():
    regex = r"([-\w]+)(([=~<>]=)|@git).*"
    logging.info(f"Verification of the dependencies in {conda_env_name.environment} conda environment")
    # Contient OBLIGATOIREMENT un '=={version}'
    actual_package_installed_list = subprocess.check_output(
        f"{CONDA_PATH} run -n {conda_env_name.environment} python -m pip freeze", shell=True).decode('utf-8')
    actual_package_installed_list = [package[0] for package in re.findall(r"([-\w]+)([=~<>]=|( @ git))", actual_package_installed_list)]

    with open(REQUIREMENT_FILE, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip() #permet de retirer les retour à la ligne
            if re.match(regex, line):
                line = re.findall(regex, line)[0][0]
            if line not in actual_package_installed_list:
                logging.info(f"{line} dependency isn't installed")
                print(f"{line} dependency isn't installed")
                return False
            line = f.readline()
    logging.info("All dependencies are installed")
    return True


def launch_metabodashboard():
    subprocess.check_call(
        f"{CONDA_PATH} run -n " + conda_env_name.environment + " python main.py", shell=True,
        stdout=subprocess.DEVNULL)


def conda_handler():
    os_used = platform.system()
    loader = Loader(desc="Checking for conda installation...").start()
    if not is_conda_installed():
        loader.stop(fail=True)
        print("conda not found !")
        with Loader(desc="Installing conda..."):
            if os_used == "Windows":
                install_miniconda_for_windows()
            elif os_used == "Linux":
                install_miniconda_for_linux()
            elif os_used == "Darwin":
                install_miniconda_for_mac_os()
    loader.stop()


def code_source_handler():
    os_used = platform.system()
    loader = Loader(desc="Checking for source code...").start()
    if not check_if_minimum_file_requirement_exist():
        loader.stop(fail=True)
        print("Source code not found !")
        with Loader(desc="\tDownloading source code..."):
            if os_used == "Windows":
                install_from_git_hub_for_windows()
            elif os_used == "Linux" or os_used == "Darwin":
                install_from_git_hub_for_linux()

        internal_loader = Loader(
            desc="\tRe-checking for source code...").start()
        if not check_if_minimum_file_requirement_exist():
            internal_loader.stop(fail=True)
            raise Exception("Source code couldn't be downloaded")
        internal_loader.stop()
    loader.stop()


def create_metabodashboard_conda_env():
    conda_env_name.environment = "metabodashboard"
    loader = Loader(desc="Checking for metabodashboard environment...").start()
    if not is_metabodashboard_env_exist():
        loader.stop(fail=True)
        print("metabodashboard environment not found !")
        with Loader(desc="\tCreating metabodashboard environment..."):
            create_metabodashboard_env()
        # with Loader(desc="\tInstalling dependencies in environment..."):
        #     try:
        #         install_dependencies()
        #     except:
        #         logging.error(
        #             f"Installation of the dependencies in {condaEnvName.environment} conda environment failed")
        #         exit(0)

        internal_loader = Loader(
            desc="Re-checking for metabodashboard environment...").start()
        if not is_metabodashboard_env_exist():
            internal_loader.stop(fail=True)
            logging.error("metabodashboard environment couldn't be created")
            raise Exception("metabodashboard environment couldn't be created")
        internal_loader.stop()
    loader.stop()


def check_other_env():
    loader = Loader(desc=f"Checking for {conda_env_name.environment} environment...").start()
    if not is_metabodashboard_env_exist():
        loader.stop(fail=True)
        print(f"Error : environment {conda_env_name.environment} not found")
        exit(1)
    loader.stop()


def dependency_handler():
    loader = Loader(desc="Checking dependencies...").start()
    if not env_dependencies_verification():
        loader.stop(fail=True)
        loader = Loader(desc="\tInstalling dependencies in environment...").start()
        try:
            install_dependencies()
        except:
            logging.error(
                f"Installation of the dependencies in {conda_env_name.environment} conda environment failed")
            loader.stop(fail=True)
            exit(1)
        loader.stop()

        internal_loader = Loader(
            desc="\tRe-checking dependencies...").start()
        if not env_dependencies_verification():
            internal_loader.stop(fail=True)
            raise Exception("Dependencies couldn't be installed")
        internal_loader.stop()
    loader.stop()


def check_python_version():
    loader = Loader(desc=f"Checking of the python version installed...").start()
    python_version = subprocess.check_output(f"{CONDA_PATH} run -n {conda_env_name.environment} python --version", shell=True).decode('utf-8')
    if "3.8" in python_version:
        logging.info("The correct version of python (3.8) is installed.")
        logging.info(f"(python version is {python_version})")
        loader.stop()
    else:
        logging.error("Wrong version of python installed, please install python 3.8")
        print(f"Wrong version of python installed {python_version}, please install python 3.8")
        loader.stop(fail=True)
        exit(1)


def main():

    conda_handler()  # Check if conda is installed, if not : download & install for appropriate OS

    # TODO : installer git
    # TODO : sortir de tout potentiel environnement (eviter un env dans un env, surtout melange venv et conda)

    code_source_handler()  # Check if code of Metabodashboard is present, if not : clone it from github

    if not conda_env_name.environment:  # Check if environment has been specified
        create_metabodashboard_conda_env()  # If not create a conda environment "metabodashboard"
    else:
        check_other_env()  # If it has been specified, check if exist

    check_python_version()  # Check that the python version in the environment (auto or custom) is 3.8

    dependency_handler()  # Check if the packages are installed, if not : installs them inside the environment

    logging.info("Successfully installed !")
    print("Successfully installed !\n")

    with Loader(desc="Metabodashboard running at http://127.0.0.1:5000... or localhost:5000 on Windows"):
        launch_metabodashboard()


if __name__ == "__main__":
    main()
