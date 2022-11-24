import os
import sys
import shutil
import glob
from utils import filepath,create_df,update_repo_info
import pandas as pd

class VCS:
    def __init__(self):
        self.RepoPath = "./GitTest"  # initialize with the current working directory
        self.git = os.path.join(self.RepoPath, ".git-vcs")
        self.repo_info=os.path.join(self.git,"repo_info.csv")
        self.files_list = list()
        self.sha_list=list()
        self.track_flag=list()
        self.is_init = False

    def initialize(self):
        self.is_init = True
        if os.path.exists(self.git):
            shutil.rmtree(self.git)
            print("Reinitializing Git ... ")

        os.mkdir(self.git)
        filepath(self.RepoPath, self.files_list,self.sha_list,self.track_flag)
        # print(self.files_list,self.sha_list,self.track_flag)
        df=create_df(self.files_list,self.sha_list,self.track_flag)
        df.to_csv(self.repo_info)

    def status(self):
        df=pd.read_csv(self.repo_info)
        # print(df)
        untrack=[]
        track=[]
        modified=[]
        for ind in df.index:
            if int(df['track_flag'][ind]) is 0:
                untrack.append(df['filename'][ind])
            elif int(df['track_flag'][ind]) is 1:
                track.append(df['filename'][ind])
            elif int(df['track_flag'][ind]) is 2:
                modified.append(df['filename'][ind])
        # print(untrack,track,modified)

    def update_repo(self):
        self.files_list.clear()
        self.sha_list.clear()
        self.track_flag.clear()
        update_repo_info(self.repo_info,self.RepoPath,self.files_list,self.sha_list,self.track_flag)
    def add(self):
        pass

    def pull(self):
        pass

    def push(self):
        pass

    def rollback(self):
        pass



    def diff(self):
        pass

    def commit(self):
        pass

    def log(self):
        pass
