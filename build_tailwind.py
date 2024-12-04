import subprocess
import os

def build_tailwind():
    """Build Tailwind CSS"""
    try:
        # Ensure the output directory exists
        os.makedirs('static/css', exist_ok=True)
        
        # Run the tailwind build command with verbose output
        result = subprocess.run([
            'npx',
            'tailwindcss',
            '-i', './static/css/src/input.css',
            '-o', './static/css/tailwind.css',
            '--minify',
            '-v'
        ], check=True, capture_output=True, text=True)
        
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("Tailwind CSS built successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error building Tailwind CSS: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    build_tailwind() 