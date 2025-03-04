"""
Format Python code.
"""

import argparse
import os
import platform
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description="Format Python code.")
parser.add_argument(
    "--dir",
    type=str,
    default=None,
    help="Directory to format (default: parent directory of the script)",
)
args = parser.parse_args()

if args.dir:
    # Get specified directory
    os.chdir(args.dir)
else:
    # Get the parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    os.chdir(parent_dir)

subprocess.run(["isort", "."], check=True)
subprocess.run(["black", "."], check=True)

time.sleep(1)
if platform.system() == "Windows":
    subprocess.run("cls", shell=True, check=True)
else:
    subprocess.run("clear", check=True)
sys.exit(0)
