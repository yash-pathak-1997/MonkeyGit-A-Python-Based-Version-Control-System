import datetime
import os
import sys
import shutil
import glob
from utils import filepath, create_df, update_repo_info, create_log_df
import pandas as pd
from Config import UnTrackedDel, UnTrackedMod, UnTrackedNew, TrackedDel, TrackedMod, TrackedNew


class File:
    def __init__(self, ID, filename, sha, track_status):
        self.ID = ID
        self.filename = filename
        self.sha = sha
        self.track_status = track_status


class VCS:
    def __init__(self, cwd):
        self.RepoPath = cwd  # initialize with the current working directory
        self.git = os.path.join(self.RepoPath, ".git-vcs")
        self.repo_info = os.path.join(self.git, "repo_info.csv")
        self.log_info = os.path.join(self.git, "log_info.csv")
        self.repo_area = os.path.join(self.git, "Repository")
        self.files_list = list()
        self.sha_list = list()
        self.track_flag = list()
        if os.path.exists(self.git):
            self.is_init = True
        else:
            self.is_init = False

    def initialize(self):
        if os.path.exists(self.git):
            shutil.rmtree(self.git)
            print("Reinitializing Git ... ")

        os.mkdir(self.git)
        os.mkdir(self.repo_area)
        filepath(self.RepoPath, self.files_list, self.sha_list, self.track_flag)

        # create repo_info.csv
        df = create_df(self.files_list, self.sha_list, self.track_flag)
        df.to_csv(self.repo_info, index=False)

        # create log_info.csv
        df_log = create_log_df(["init"], [datetime.datetime.now()], ["NA"])
        df_log.to_csv(self.log_info, index=False)

    def status(self):
        df = pd.read_csv(self.repo_info)

        u0_list = df[df["track_flag"] == "U0"]['filename'].to_list()
        u1_list = df[df["track_flag"] == "U1"]['filename'].to_list()
        u2_list = df[df["track_flag"] == "U2"]['filename'].to_list()
        t0_list = df[df["track_flag"] == "T0"]['filename'].to_list()
        t1_list = df[df["track_flag"] == "T1"]['filename'].to_list()
        t2_list = df[df["track_flag"] == "T2"]['filename'].to_list()

        res = {
            "untracked_new": u0_list,
            "untracked_mod": u1_list,
            "untracked_del": u2_list,
            "tracked_new": t0_list,
            "tracked_mod": t1_list,
            "tracked_del": t2_list
        }

        return res

    def update_repo(self):
        update_repo_info(self.repo_info, self.RepoPath, self.files_list, self.sha_list, self.track_flag)
        df = create_df(self.files_list, self.sha_list, self.track_flag)
        print(df)
        df.to_csv(self.repo_info)

    def print(self):
        # read repo info
        df = pd.read_csv(self.repo_info)
        people = df.to_records(index=False)

        # revert and write back
        final_df = pd.DataFrame(people).iloc[:, 1:]
        print(final_df)

    def add(self, arg_list):
        df = pd.read_csv(self.repo_info)
        if arg_list[0] == '.':
            for ind in df.index:
                if df['track_flag'][ind] == UnTrackedNew:
                    df['track_flag'][ind] = TrackedNew
                if df['track_flag'][ind] == UnTrackedMod:
                    df['track_flag'][ind] = TrackedMod
        else:
            for filename in arg_list:
                for ind in df.index:
                    if df['filename'][ind] == filename:
                        if df['track_flag'][ind] == UnTrackedNew:
                            df['track_flag'][ind] = TrackedNew
                        if df['track_flag'][ind] == UnTrackedMod:
                            df['track_flag'][ind] = TrackedMod

    def log(self, cmd):
        insert_obj = {
            "Command": cmd,
            "Timestamp": datetime.datetime.now(),
            "CommitId": "NA"
        }
        insert_obj = pd.json_normalize(insert_obj)

        df = pd.read_csv(self.log_info)
        df = pd.concat([df, insert_obj], ignore_index=True)
        df["ID"] = df.index
        df.to_csv(self.log_info, index=False)

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