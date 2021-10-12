##https://github.com/pineappleEA/pineapple-src
from YuzuUpdater.YuzuGithubRepoAPi import YuzuUpdater
import os
import sys

def main():
    
    if getattr(sys, 'frozen', False):
        ROOT_DIR = os.path.dirname(os.path.abspath(sys.executable))
    elif __file__:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    updater = YuzuUpdater(rootPath=ROOT_DIR)
    updater.downloadLastRelease()

if __name__ == "__main__":
    main()
