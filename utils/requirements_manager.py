import pkg_resources
import subprocess
import os
from datetime import datetime

def get_installed_packages():
    """Get a list of all installed packages and their versions."""
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

def write_requirements(packages):
    """Write packages to requirements.txt file."""
    with open('requirements.txt', 'w') as f:
        f.write(f'# Auto-generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        for package, version in sorted(packages.items()):
            f.write(f'{package}=={version}\n')

def update_requirements():
    """Update requirements.txt with currently installed packages."""
    try:
        # Get currently installed packages
        current_packages = get_installed_packages()
        
        # Read existing requirements.txt if it exists
        existing_packages = {}
        if os.path.exists('requirements.txt'):
            with open('requirements.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            package, version = line.split('==')
                            existing_packages[package] = version
                        except ValueError:
                            continue

        # Check if there are any changes
        if current_packages != existing_packages:
            write_requirements(current_packages)
            print("requirements.txt has been updated with current package versions")
        else:
            print("requirements.txt is up to date")
            
    except Exception as e:
        print(f"Error updating requirements.txt: {str(e)}")
