# -*- coding: utf-8 -*-
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import threading
from itertools import cycle
from time import sleep
import webbrowser

try:  # Try to import the module tqdm and install it if it is not already installed
    from tqdm import tqdm
except ImportError:
    logging.info("tqdm not found, installing it")
    subprocess.call(
        f"{sys.executable} -m pip install tqdm", shell=True, stdout=subprocess.DEVNULL
    )
    try:
        from tqdm import tqdm
    except ImportError:
        logging.error("tqdm failed to install")
        sys.exit(1)

try:  # Try to import the module requests and install it if it is not already installed
    import requests
except ImportError:
    logging.info("requests not found, installing it")
    subprocess.call(
        f"{sys.executable} -m pip install requests",
        shell=True,
        stdout=subprocess.DEVNULL,
    )
    try:
        import requests
    except ImportError:
        logging.error("requests failed to install")
        sys.exit(1)

try:  # Try to import the module argparse and install it if it is not already installed
    import argparse
except ImportError:
    logging.info("argparse not found, installing it")
    subprocess.call(
        f"{sys.executable} -m pip install argparse",
        shell=True,
        stdout=subprocess.DEVNULL,
    )
    try:
        import argparse
    except ImportError:
        logging.error("argparse failed to install")
        sys.exit(1)

RO_TEMP_TOKEN = "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"

# file containing the list of packages to install in the conda environment for MeDIC
REQUIREMENT_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "requirements.txt")
)

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
MINICONDA_FILE = os.path.abspath(os.path.join(ROOT_DIR, "Miniconda3-latest"))
CONDA_PATH = "conda"

# setup parser for command line arguments
parser = argparse.ArgumentParser(description="Installation parameter")
parser.add_argument("-e", "--environment", help="Conda environment name")
parser.add_argument(
    "-l", "--no-launch", help="Install without launching ", action="store_true"
)
parser.add_argument(
    "-c", "--no-check", help="Install without checking environment", action="store_true"
)
parser.add_argument(
    "-u",
    "--update",
    help="Update to last version available on GitHub",
    action="store_true",
)
arg = parser.parse_args()

# setup constants from parameters
env_name_not_set = False if arg.environment else True
conda_env_name = arg.environment if arg.environment else "medic"
no_launch = arg.no_launch
no_check = arg.no_check
update = arg.update

# setup logging file content and format
logging.basicConfig(
    level=logging.INFO,
    filename="MeDIC_Installation.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(funcName)s (ligne %(lineno)d) - %(message)s",
)

SEPARATOR = "|"


# runs the command in the correct conda environment
def conda_command(command: str):
    return f"{CONDA_PATH} activate {conda_env_name} {SEPARATOR} {command}"


# runs the python command in the correct conda environment
def in_env_python_command(command: str, is_module: bool = True):
    return conda_command(f"python {'-m' if is_module else ''} {command}")


class Loader:
    def __init__(
        self,
        desc="Loading...",
        end="checked",
        fail="fail",
        timeout=0.1,
        installation=True,
    ):
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

        self.steps = [
            "|MeDIC installation ...     |",
            "| MeDIC installation ...    |",
            "|  MeDIC installation ...   |",
            "|   MeDIC installation ...  |",
            "|    MeDIC installation ... |",
            "|     MeDIC installation ...|",
            "|      MeDIC installation ..|",
            "|.      MeDIC installation .|",
            "|..      MeDIC installation |",
            "|...      MeDIC installation|",
            "| ...      MeDIC installatio|",
            "|n ...      MeDIC installati|",
            "|on ...      MeDIC installat|",
            "|ion ...      MeDIC installa|",
            "|tion ...      MeDIC install|",
            "|ation ...      MeDIC instal|",
            "|lation ...      MeDIC insta|",
            "|llation ...      MeDIC inst|",
            "|allation ...      MeDIC ins|",
            "|tallation ...      MeDIC in|",
            "|stallation ...      MeDIC i|",
            "|nstallation ...      MeDIC |",
            "|installation ...      MeDIC|",
            "| installation ...      MeDI|",
            "|C installation ...      MeD|",
            "|IC installation ...      Me|",
            "|DIC installation ...      M|",
            "|EDIC installation ...      |",
        ]

        if not installation:
            self.steps = [
                "|MeDIC  |",
                "| MeDIC |",
                "|  MeDIC|",
                "|   MeDI|",
                "|C   MeD|",
                "|IC   Me|",
                "|DIC   M|",
                "|eDIC   |",
            ]

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
        print(
            f"\r{self.desc}       {self.end if not fail else self.fail}                               ",
            flush=True,
        )

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


# Check if MeDIC's files are already here
def check_if_minimum_file_requirement_exist():
    logging.info("Checking if the github repository is already downloaded")
    return os.path.exists("medic") and os.path.exists("requirements.txt")


# Check if Git is already installed
def check_if_git_folder_exist():
    logging.info("Checking if the git folder is already downloaded")
    return os.path.exists(".git")


# Install MiniConda
def download_miniconda(url_for_download: str, extension: str = ".sh"):
    logging.info("Downloading MiniConda")
    request = requests.get(url_for_download)
    with open(MINICONDA_FILE + extension, "wb") as exe_file:
        exe_file.write(request.content)


# Download the latest version of MiniConda for Windows, install it and set the path variable
def install_miniconda_for_windows():
    logging.info("Start downloading MiniConda for Windows")
    conda_for_windows = (
        f"https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86"
        f"{'_64' if is_os_64bit() else ''}.exe"
    )
    download_miniconda(conda_for_windows, extension=".exe")
    logging.info("MiniConda for Windows downloaded")

    logging.info("Installing MiniConda for Windows")
    install_conda_command = (
        f"start /wait {MINICONDA_FILE + '.exe'} /InstallationType=JustMe /RegisterPython=0 "
        f"/S /AddToPath=1 /D=%UserProfile%\\Miniconda3"
    )
    subprocess.check_call(install_conda_command, shell=True, stdout=subprocess.DEVNULL)
    subprocess.check_call(
        "SET PATH=%PATH%;%UserProfile%\\Miniconda3\\Library\\bin",
        shell=True,
        stdout=subprocess.DEVNULL,
    )
    logging.info("MiniConda for Windows installed")

    logging.info("Setting the path variable")
    global CONDA_PATH  # Set the path to avoid needing to restart the terminal to refresh the path variable
    CONDA_PATH = "%UserProfile%\\Miniconda3\\Library\\bin\\conda"
    logging.info("Path variable set")


# Download the latest version of MiniConda for Linux, install it and set the path variable
def install_miniconda_for_linux():
    logging.info("Start downloading MiniConda for Linux")
    conda_for_linux = (
        f"https:F//repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86"
        f"{'_64' if is_os_64bit() else ''}.sh "
    )
    download_miniconda(conda_for_linux)
    logging.info("MiniConda for Linux downloaded")

    logging.info("Installing MiniConda for Linux")
    install_conda_command = f"bash {MINICONDA_FILE + '.sh -b -p ~/miniconda3'}"
    subprocess.check_call(install_conda_command, shell=True)
    subprocess.check_call(
        "export PATH='~/miniconda3/bin:$PATH'", shell=True, stdout=subprocess.DEVNULL
    )
    logging.info("MiniConda for Linux installed")

    logging.info("Setting the path variable")
    global CONDA_PATH  # Set the path to avoid needing to restart the terminal to refresh the path variable
    CONDA_PATH = "~/miniconda3/bin/conda"
    logging.info("Path variable set")


# Download the latest version of Miniconda for macOS, install it and set the path variable
def install_miniconda_for_mac_os():
    logging.info("Start downloading MiniConda for macOS")
    conda_for_macos = (
        f"https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86"
        f"{'_64' if is_os_64bit() else ''}.sh "
    )
    download_miniconda(conda_for_macos)
    logging.info("MiniConda for macOS downloaded")

    logging.info("Installing MiniConda for MacOs")
    install_conda_command = f"bash {MINICONDA_FILE + '.sh'}"
    subprocess.check_call(install_conda_command, shell=True)
    subprocess.check_call(
        "export PATH='~/miniconda3/bin:$PATH'", shell=True, stdout=subprocess.DEVNULL
    )
    logging.info("MiniConda for MacOs installed")

    logging.info("Setting the path variable")

    global CONDA_PATH
    CONDA_PATH = "~/miniconda3/bin/conda"
    logging.info("Path variable set")


# Check if conda is already installed
def is_conda_installed() -> bool:
    logging.info("Checking for conda installation")
    try:
        subprocess.check_call(
            f"{CONDA_PATH} env list", shell=True, stdout=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        logging.info("Cannot find conda")
        return False
    logging.info("Conda found")
    return True


# Check if the environment exists
def is_medic_env_exist() -> bool:
    logging.info(f"Checking for {conda_env_name} conda environment")
    envi_list = subprocess.check_output(f"{CONDA_PATH} env list", shell=True)
    if "\n" + conda_env_name + " " in envi_list.decode("utf-8").lower():
        logging.info(f"{conda_env_name} conda environment found")
        return True
    logging.info(f"{conda_env_name} conda environment not found")
    return False


# Create the MeDIC conda environment
def create_MeDIC_env():
    logging.info("MeDIC conda environment creation")
    subprocess.check_call(
        f"{CONDA_PATH} create -n MeDIC -y python=3.8",
        shell=True,
        stdout=subprocess.DEVNULL,
    )


# Install the dependency in the conda environment or update them
def install_dependency(dependency: str, upgrade: bool):
    logging.info(f"Installing {dependency}")
    subprocess.check_call(
        in_env_python_command(
            f"pip install {dependency} {'--upgrade' if upgrade else ''}"
        ),
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    logging.info(f"{dependency} installed")


# Install the dependencies in the conda environment or update them
def install_dependencies(upgrade: bool = False):
    thread_list = []
    logging.info(
        f"Installation of the dependencies in {conda_env_name} conda environment"
    )
    with open(REQUIREMENT_FILE, "r") as f:
        lines = f.readlines()
    for dependency in tqdm(lines, desc="Installing dependencies "):
        try:
            dependency_thread = threading.Thread(
                target=install_dependency, args=(dependency, upgrade)
            )
            dependency_thread.start()
            thread_list.append(dependency_thread)
        except subprocess.CalledProcessError as err:
            logging.error(err)
            raise ImportError(dependency)
    for thread in thread_list:
        thread.join()
    logging.info("All dependencies have been installed")


# Check if the system is 64-bit
def is_os_64bit():
    return platform.machine().endswith("64")


# Check if the environment is already setup
def env_dependencies_verification():
    regex = r"([-\w]+)(([=~<>]=)|@git).*"
    logging.info(
        f"Verification of the dependencies in {conda_env_name} conda environment"
    )
    # Contient OBLIGATOIREMENT un '=={version}'
    actual_package_installed_list = subprocess.check_output(
        in_env_python_command("pip freeze"), shell=True
    ).decode("utf-8")
    actual_package_installed_list = [
        package[0]
        for package in re.findall(
            r"([-\w]+)([=~<>]=|( @ git))", actual_package_installed_list
        )
    ]

    with open(REQUIREMENT_FILE, "r") as f:
        line = f.readline()
        while line:
            line = line.strip().replace("_", "-")  # remove endline and replace _ by -
            if re.match(regex, line):
                line = re.findall(regex, line)[0][0]
            if line not in actual_package_installed_list:
                logging.info(f"{line} dependency isn't installed")
                return False
            line = f.readline()
    logging.info("All dependencies are installed")
    return True


# Move the files to the correct directory next to the launcher from the download folder
def move_files_from_clone_to_project_folder():
    all_content = os.listdir("./temporary_installation_folder/")
    here_content = os.listdir("./")

    for item in all_content:
        for here_item in here_content:
            if item == here_item:
                os.remove(f"./{item}")
        os.rename("./temporary_installation_folder/" + item, "./" + item)


# Download MeDIC from the GitHub repository
def install_from_github_on_os():
    logging.info("Downloading project file from github")

    try:
        os.remove("./temporary_installation_folder")
    except FileNotFoundError:
        pass

    subprocess.check_call(
        "git clone -q "
        f"https://{RO_TEMP_TOKEN + '@'}github.com/ElinaFF/MetaboDashboard "
        f"temporary_installation_folder",
        shell=True,
        stdout=subprocess.DEVNULL,
    )

    move_files_from_clone_to_project_folder()


# Download MeDIC from the GitHub repository for update
def pull_from_github():
    logging.info("Pulling project file from github")
    loader = Loader(desc="Updating project...").start()
    if check_if_git_folder_exist():
        subprocess.check_call(
            f"git pull -q https://{RO_TEMP_TOKEN + '@'}github.com/ElinaFF/MetaboDashboard",
            shell=True,
            stdout=subprocess.DEVNULL,
        )
        logging.info("Project updated")
        loader.stop()
    else:
        logging.info("Couldn't find the .git folder")
        loader.stop(fail=True)


# Open the webpage in the browser after starting the server
def startWebPage():
    # Wait 10 seconds to let the server start before opening the browser to avoid browser timeout
    sleep(10)
    webbrowser.open("http://127.0.0.1:5000")
    logging.info("Web page opened")


# Launch the server and open the webpage
def launch_medic():
    start_web_page_thread = threading.Thread(
        target=startWebPage
    )  # Creation of a thread to start the web page
    start_web_page_thread.start()  # Start of the thread
    subprocess.check_call(
        in_env_python_command("main.py", is_module=False),
        shell=True,
        stdout=subprocess.DEVNULL,
    )


# Check if Conda is installed and install it if necessary
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


# Raise an error if the required files are not found
def raise_error_if_minimum_file_requirement_exist(internal_loader):
    if not check_if_minimum_file_requirement_exist():
        internal_loader.stop(fail=True)
        raise Exception("Source code couldn't be downloaded")


# Check if the minimum files are present and install them if necessary
def code_source_handler():
    loader = Loader(desc="Checking for source code...").start()
    if not check_if_minimum_file_requirement_exist():
        loader.stop(fail=True)
        print("Source code not found !")
        with Loader(desc="\tDownloading source code..."):
            install_from_github_on_os()
        internal_loader = Loader(desc="\tRe-checking for source code...").start()
        raise_error_if_minimum_file_requirement_exist(internal_loader)
        internal_loader.stop()
    loader.stop()


# Raise an error if the environment is still not present
def raise_error_if_env_still_does_not_exist(internal_loader):
    if not is_medic_env_exist():
        internal_loader.stop(fail=True)
        logging.error("medic environment couldn't be created")
        raise Exception("medic environment couldn't be created")


# Creat the MeDIC environment if not detected
def create_medic_conda_env():
    loader = Loader(desc="Checking for medic environment...").start()
    if not is_medic_env_exist():
        loader.stop(fail=True)
        print("medic environment not found !")
        with Loader(desc="\tCreating medic environment..."):
            create_MeDIC_env()
        internal_loader = Loader(desc="\tRe-checking for medic environment...").start()
        raise_error_if_env_still_does_not_exist(internal_loader)
        internal_loader.stop()
    loader.stop()


# Check if the custom environment exists
def check_other_env():
    loader = Loader(desc=f"Checking for {conda_env_name} environment...").start()
    if not is_medic_env_exist():
        loader.stop(fail=True)
        print(f"Error : environment {conda_env_name} not found")
        exit(1)
    loader.stop()


# Raise an error if the dependencies are not correctly installed
def raise_error_if_can_not_install_dependencies(internal_loader):
    if not env_dependencies_verification():
        internal_loader.stop(fail=True)
        raise Exception("Dependencies couldn't be installed")


# Update the dependencies of the environment if the update parameter is True
def install_dependencies_or_raise_error(upgrade: bool = False):
    try:
        install_dependencies(upgrade)
    except ImportError as problematicPackage:
        logging.error(
            f"Installation of the dependencies {problematicPackage} in {conda_env_name} conda environment failed"
        )
        print(f"Error while installing {problematicPackage}")
        exit(1)


# Check if the dependencies are installed and install them if necessary
def dependency_handler(upgrade: bool = False):
    loader = Loader(desc="Checking dependencies...").start()
    if not env_dependencies_verification() or upgrade:
        loader.stop(fail=True)
        install_dependencies_or_raise_error(upgrade)
        loader.stop()
        internal_loader = Loader(desc="\tRe-checking dependencies...").start()
        raise_error_if_can_not_install_dependencies(internal_loader)
        internal_loader.stop()
    loader.stop()


# Check if the right version of Python is installed
def check_python_version():
    loader = Loader(desc=f"Checking of the python version installed...").start()
    python_version = subprocess.check_output(
        in_env_python_command("--version", is_module=False), shell=True
    ).decode("utf-8")
    if "3.8" in python_version:
        logging.info("The correct version of python (3.8) is installed.")
        logging.info(f"(python version is {python_version})")
        loader.stop()
    else:
        logging.error("Wrong version of python installed, please install python 3.8")
        print(
            f"Wrong version of python installed {python_version}, please install python 3.8"
        )
        loader.stop(fail=True)
        exit(1)


# Core function of the Launcher, starts all the processes in the right order
def main():
    if platform.system() == "Windows":
        global SEPARATOR
        SEPARATOR = "&"

    if no_check:
        if not no_launch:
            with Loader(
                desc="MeDIC running at http://127.0.0.1:5000... or localhost:5000 on Windows",
                installation=False,
            ):
                launch_medic()
        exit(0)

    if update:
        pull_from_github()
        dependency_handler(upgrade=True)
        exit(0)

    # Creation of the thread that will run the conda handler
    conda_handler_thread = threading.Thread(target=conda_handler)
    # Check if conda is installed, if not : download & install for appropriate OS
    conda_handler_thread.start()  # Start the thread

    # TODO : sortir de tout potentiel environnement (eviter un env dans un env, surtout melange venv et conda)

    # Creation of the thread that will run the code source handler
    code_source_handler_thread = threading.Thread(target=code_source_handler)
    # Check if code of MeDIC is present, if not : clone it from GitHub
    code_source_handler_thread.start()  # Start the thread

    conda_handler_thread.join()  # Wait for the thread to finish as the following code require Conda

    if env_name_not_set:  # Check if environment has been specified
        create_medic_conda_env()  # If not create a conda environment "medic"
    else:
        check_other_env()  # If it has been specified, check if exist

    # check_python_version()  # Check that the python version in the environment (auto or custom) is 3.8

    dependency_handler()  # Check if the packages are installed, if not : installs them inside the environment

    code_source_handler_thread.join()  # Wait for the thread to finish to fully finish the installation

    logging.info("Successfully installed !")
    print("Successfully installed !\n")

    if no_launch:
        exit(0)

    with Loader(
        desc="MeDIC running at http://127.0.0.1:5000... or localhost:5000 on Windows",
        installation=False,
    ):
        launch_medic()


if __name__ == "__main__":
    main()
