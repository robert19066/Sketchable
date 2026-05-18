import string
import subprocess
import sys
import os

class Helmet:
    """
    Class for making python files into executables.
    [EXPERIMENTAL]
    and yes i might deleate it, like Ticky. 
    """
    def __init__(self):
        pass
    
    def build(self, distpath: str):
        print("Building file via Helmet.")
        print("Powered by Pyinstaller")
        subprocess.run([sys.executable, 'python', '-m', 'pyinstaller', '--onefile', '--dist-dir', distpath], check=True)
