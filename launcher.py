import os

import pkg_resources

with open('requirement.txt', 'r') as f:
    requirements = f.read().splitlines()


if __name__ == "__main__":
    print("MetaboDashboard is starting...")
    print()
    print("Checking dependencies...")
    try:
        pkg_resources.require(requirements)
    except pkg_resources.DistributionNotFound:
        print("Dependencies not found. Installation is starting...")
        print()
        os.system("pip install -r requirement.txt")
        try:
            pkg_resources.require(requirements)
        except pkg_resources.DistributionNotFound as error:
            print()
            print("Installation failed with error:", str(error))
            print("Please install MetaboDashboard dependencies manually.")
            exit()

    print("Dependencies are OK.")
    print()

    from metabodashboard import app

    app.run_server(debug=True, port=8080, host='localhost')
