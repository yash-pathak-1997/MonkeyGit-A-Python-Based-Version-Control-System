import os
import sys


class VCS:
    def __init__(self):
        self.RepoPath = os.getcwd()  # initialize with the current working directory
        self.git = os.path.join(self.RepoPath, ".git-vcs")

    def initialize(self):
        if not os.path.exists(self.git):
            os.mkdir(self.git)
        else:
            print("Git Repository has already been initialized!!")
            sys.exit(0)

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
