import os
import sys
import shutil
import glob
from utils import filepath, create_df, update_repo_info
import pandas as pd
from Config import UnTrackedDel,UnTrackedMod,UnTrackedNew,TrackedDel,TrackedMod,TrackedNew


class VCS:
    def __init__(self, cwd):
        self.RepoPath = cwd  # initialize with the current working directory
        self.git = os.path.join(self.RepoPath, ".git-vcs")
        self.repo_info = os.path.join(self.git, "repo_info.csv")
        self.files_list = list()
        self.sha_list = list()
        self.track_flag = list()
        self.is_init = True

    def initialize(self):
        self.is_init = True
        if os.path.exists(self.git):
            shutil.rmtree(self.git)
            print("Reinitializing Git ... ")

        os.mkdir(self.git)
        filepath(self.RepoPath, self.files_list, self.sha_list, self.track_flag)
        df = create_df(self.files_list, self.sha_list, self.track_flag)
        df.to_csv(self.repo_info)
        print("Self", self.files_list, self.sha_list, self.track_flag)

    def status(self):
        df = pd.read_csv(self.repo_info)
        # print(df)
        untrack = []
        track = []
        modified = []

        for ind in df.index:
            if df['track_flag'][ind] is "U0":
                untrack.append(df['filename'][ind])
            elif df['track_flag'][ind] is "U1":
                track.append(df['filename'][ind])
            elif df['track_flag'][ind] is "U2":
                modified.append(df['filename'][ind])
        # print(untrack,track,modified)

    def update_repo(self):
        update_repo_info(self.repo_info, self.RepoPath, self.files_list, self.sha_list, self.track_flag)
        df = create_df(self.files_list, self.sha_list, self.track_flag)
        print(df)
        df.to_csv(self.repo_info)

    def add(self, arg_list):
        df = pd.read_csv(self.repo_info)
        temp = df
        flag = 0
        if arg_list[0] == '.':
            print("Added all")
            for ind in df.index:
                # if df['track_flag'][ind]!="1":
                if df['track_flag'][ind] == "3":
                    temp.drop(temp.index[ind - flag], inplace=True)
                    flag = flag + 1
                else:
                    temp['track_flag'][ind - flag] = "1"
        else:
            for name in arg_list:
                for ind in df.index:
                    if df['filename'][ind] == name:
                        if df['track_flag'][ind] == "3":
                            temp.drop(temp.index[ind - flag], inplace=True)
                            flag = flag + 1
                        else:
                            temp['track_flag'][ind - flag] = "1"
        df = temp
        df.to_csv(self.repo_info)

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
