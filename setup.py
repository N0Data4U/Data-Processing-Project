import subprocess

# Creating virtual environment
subprocess.run(["python", "-m", "venv", "ENV"])

# Installing module requirements
subprocess.run(["pip", "install", "-r", "requirements.txt"])