import subprocess
import os
import threading
import pkg_resources

def install_pip_requirements():
    """Install Python dependencies if they are not already installed."""
    with open('requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    packages_to_install = [pkg for pkg in required_packages if pkg not in installed_packages]
    if packages_to_install:
        subprocess.run('pip install -r requirements.txt', shell=True)
    else:
        print("All Python dependencies are already installed.")

def install_npm_dependencies():
    """Install Node.js dependencies if they are not already installed."""
    node_modules_path = os.path.join('file-upload-app', 'node_modules')
    if not os.path.exists(node_modules_path):
        subprocess.run('npm install', cwd='file-upload-app', shell=True)
    else:
        print("All Node.js dependencies are already installed.")

def run_uvicorn_server():
    """Run the Uvicorn server."""
    subprocess.run('uvicorn app:app --reload', shell=True)

def run_npm_start():
    """Run the frontend application."""
    subprocess.run('npm start', cwd='file-upload-app', shell=True)

if __name__ == '__main__':
    # Install dependencies if needed
    install_pip_requirements()
    install_npm_dependencies()

    # Start backend and frontend in separate threads
    uvicorn_thread = threading.Thread(target=run_uvicorn_server)
    npm_thread = threading.Thread(target=run_npm_start)
    uvicorn_thread.start()
    npm_thread.start()

    # Keep the main thread alive while subprocesses are running
    try:
        uvicorn_thread.join()
        npm_thread.join()
    except KeyboardInterrupt:
        print("Shutting down applications.")
