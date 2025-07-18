import PyInstaller.__main__
from json import load
from os.path import abspath, dirname
import os


# sets file name and assets path (from config.json)
with open(abspath(f"{dirname(__file__)}/config.json")) as f: config = load(f)
file_name = f'Scoundrel-v{config['version-number']}'
assets = "assets" if not config['demo'] else "demo_assets"

# sets the directory the build will be stored in
directory = abspath(f"builds/{file_name}")

# sets the icon image
icon = abspath(f"icon.ico")

# defines the base run command
command = [
    '--distpath', directory,
    '--name', file_name,
    '--icon', icon,
    '--clean',
    '--onefile',
    'scoundrel.py'
]

# adds all assets and resources
for file in os.listdir(abspath(f"{assets}/lang")):
    command.append("--add-data")
    command.append(f"{assets}/lang/{file}:{assets}/lang/")
for file in os.listdir(abspath(f"{dirname(__file__)}/{assets}/scripts")):
    command.append("--add-data")
    command.append(f"{assets}/scripts/{file}:{assets}/scripts/")
for file in os.listdir(abspath(f"{dirname(__file__)}/{assets}/sounds")):
    command.append("--add-data")
    command.append(f"{assets}/sounds/{file}:{assets}/sounds/")
for file in os.listdir(abspath(f"{dirname(__file__)}/{assets}/sprites")):
    command.append("--add-data")
    command.append(f"{assets}/sprites/{file}:{assets}/sprites/")

for file in os.listdir(abspath(f"{dirname(__file__)}/data")):
    command.append("--add-data")
    command.append(f"data/{file}:data/")

command.append("--add-data")
command.append("config.json:./")


# Builds the script
if __name__ == '__main__': PyInstaller.__main__.run(command)
