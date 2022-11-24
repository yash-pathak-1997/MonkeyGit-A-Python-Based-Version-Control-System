import os
import sys
import shutil
import glob
from utils import filepath


class VCS:
    def __init__(self):
        self.RepoPath = "./GitTest"  # initialize with the current working directory
        self.git = os.path.join(self.RepoPath, ".git-vcs")
        self.files_list = list()

    def initialize(self):
        if os.path.exists(self.git):
            shutil.rmtree(self.git)
            print("Reinitializing Git ... ")

        os.mkdir(self.git)
        filepath(self.RepoPath, self.files_list)
        print(self.files_list)

    def add(self):
        pass

    def pull(self):
        pass

    def push(self):
        pass

    def rollback(self):
        pass

    def status(self):
        pass

    def diff(self):
        pass

    def commit(self):
        pass

    def log(self):
        pass
