import os

try:
    from metabodashboard import app
except ImportError:
    os.system("pip install git+https://github.com/ElinaFF/MetaboDashboard.git@refactoring")
    from metabodashboard import app

if __name__ == "__main__":
    app.run_server(debug=True, port=8080, host='0.0.0.0')

