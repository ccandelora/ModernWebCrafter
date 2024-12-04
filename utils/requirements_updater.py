import pkg_resources
import subprocess
from pathlib import Path

def get_installed_packages():
    """Get a list of all installed packages and their versions."""
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

def write_requirements(packages):
    """Write the packages to requirements.txt."""
    requirements_path = Path('requirements.txt')
    with open(requirements_path, 'w') as f:
        for package, version in sorted(packages.items()):
            f.write(f"{package}=={version}\n")

def update_requirements():
    """Update requirements.txt with current package versions."""
    try:
        installed_packages = get_installed_packages()
        write_requirements(installed_packages)
        print("Requirements.txt has been updated successfully!")
        return True
    except Exception as e:
        print(f"Error updating requirements.txt: {str(e)}")
        return False

if __name__ == "__main__":
    update_requirements()
