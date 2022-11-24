import os
import sys
class VCS:
    def __init__(self):
        self.RepoPath=os.getcwd() #initialize with the current working directory
        self.git=os.path.join(self.RepoPath,".git")

    def initialize(self):
        if not os.path.exists(self.git):
            os.mkdir(self.git)
        else:
            print("Git Repository has already been initialized!!")
            sys.exit(0)