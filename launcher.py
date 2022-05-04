import os
import pkg_resources

REQUIREMENT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'requirements.txt'))


def main():
    # TODO : impossible de run avec la commande python3
    print("\033[33m{}\033[00m".format("WARNING : This script is not compatible with the command python3"))
    print()
    print("MetaboDashboard is starting...")
    print()
    print("Checking dependencies...")

    with open(REQUIREMENT_FILE, 'r') as f:
        requirements = f.read().splitlines()
    try:
        pkg_resources.require(requirements)
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        print("Dependencies not found. Installation is starting...")
        print()
        os.system("pip install -r " + REQUIREMENT_FILE)
        try:
            pkg_resources.require(requirements)
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict) as error:
            print()
            print("Installation failed with error:", str(error))
            print("Please install MetaboDashboard dependencies manually.")
            exit()

    print("Dependencies are OK.")
    print()
    print("Server is starting...")
    print()
    from metabodashboard import app
    app.run_server(debug=True, host='127.0.0.1', port=5000)


if __name__ == "__main__":
    main()
