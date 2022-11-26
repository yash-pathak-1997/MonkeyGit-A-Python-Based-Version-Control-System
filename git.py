import datetime
import hashlib
import os
import sys
import json
import shutil
import glob
import datetime
import time
from utils import filepath, create_df, update_repo_info, create_log_df
import pandas as pd
from Config import conf_obj,UnTrackedDel, UnTrackedMod, UnTrackedNew, TrackedDel, TrackedMod, TrackedNew


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
        self.commit_area=os.path.join(self.git, "Commit")
        self.commit_head=os.path.join(self.git,"commit_head.txt")
        self.commit_info=os.path.join(self.git,"commit_info.json")
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
        os.mkdir(self.commit_area)
        f=open(self.commit_head,"w")
        f.write("null")
        f = open(self.commit_info, "w")
        f.write("{}")
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
        cwd = conf_obj["cwd"]
        if arg_list[0] == '.':
            for ind in df.index:
                flag = 0
                if df['track_flag'][ind] == UnTrackedNew:
                    df.at[ind, 'track_flag'] = TrackedNew
                    flag = 1
                if df['track_flag'][ind] == UnTrackedMod:
                    df.at[ind, 'track_flag'] = TrackedMod
                    flag = 1
                if df['track_flag'][ind] == UnTrackedDel:
                    df.at[ind, 'track_flag'] = TrackedDel
                    flag = 1
                if flag == 1:
                    f = open(
                        os.path.join(self.repo_area, df["sha"][ind] + '.' + str(df["filename"][ind]).split(".")[1]),
                        "w")
                    fread = open(df["filename"][ind], "r")
                    f.write(fread.read())

                    f.close()
                    fread.close()
        else:
            print(arg_list)
            for filename in arg_list:
                flag = 0
                for ind in df.index:
                    print(os.path.join(cwd, filename))
                    if df['filename'][ind] in os.path.join(cwd, filename):
                        print("file found")
                        if df['track_flag'][ind] == UnTrackedNew:
                            df.at[ind, 'track_flag'] = TrackedNew
                            print("untracked new", df['track_flag'][ind])
                            flag = 1
                        if df['track_flag'][ind] == UnTrackedMod:
                            df.at[ind, 'track_flag'] = TrackedMod
                            flag = 1
                        if df['track_flag'][ind] == UnTrackedDel:
                            df.at[ind, 'track_flag'] = TrackedDel
                            flag = 1
                        if flag == 1:
                            f = open(
                                os.path.join(self.repo_area,
                                             df["sha"][ind] + '.' + str(df["filename"][ind]).split(".")[1]),
                                "w")
                            fread = open(df["filename"][ind], "r")
                            f.write(fread.read())

                            f.close()
                            fread.close()
        # file_list = df["filename"].to_list()
        # sha_list = df["sha"].to_list()
        # track_flag = df["track_flag"].to_list()
        # print("length of file_list", len(file_list), len(track_flag))
        # prevf = ""
        # prevs = ""
        # prevt = ""
        # del_list = []
        for filename in arg_list:
            file_list = df["filename"].to_list()
            sha_list = df["sha"].to_list()
            track_flag = df["track_flag"].to_list()
            print("length of file_list", len(file_list), len(track_flag))
            prevf = ""
            prevs = ""
            prevt = ""
            del_list = []
            for i in range(0, len(file_list)):
                print("file index ", i)
                print(os.path.join(cwd, filename).replace("./", ''), " ", file_list[i])
                if os.path.join(cwd, filename).replace("./", '') == file_list[i] and track_flag[i] in [TrackedNew,
                                                                                                       TrackedMod]:
                    prevf = file_list[i]
                    prevs = sha_list[i]
                    prevt = track_flag[i]
                    del_list.append(i)
            print(del_list,prevf, prevs, prevt)
            f = 0
            for i in del_list:
                del file_list[i - f]
                del sha_list[i - f]
                del track_flag[i - f]
                f = f + 1
            file_list.append(prevf)
            sha_list.append(prevs)
            track_flag.append(prevt)

        new_df = pd.DataFrame()
        new_df["filename"] = file_list
        new_df["sha"] = sha_list
        new_df["track_flag"] = track_flag
        df = new_df
        df.to_csv(self.repo_info)

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

    def commit(self):
        time_stamp=str(time.time())
        t_encrypt=time_stamp.encode("utf-8")
        hash_obj=hashlib.sha256()
        hash_obj.update(t_encrypt)
        commit_folder_name=hash_obj.hexdigest()
        commit_version=os.path.join(self.commit_area,commit_folder_name)
        os.mkdir(commit_version)
        shutil.copy(self.repo_info,commit_version)
        # f_commit_head=open(self.commit_head,"r")
        # f_commit_info = open(self.commit_head, "w")
        # curr_head=f_commit_head.read()
        # print("current head is -> "+curr_head)
        # commit_pair=json.load(f_commit_info)
        # print("commit pair is -> " + commit_pair)
        # commit_pair[commit_folder_name]=curr_head
        # curr_head=commit_folder_name
        # f_commit_info.write(commit_pair)
        # f_commit_head.close()
        # f_commit_head=open(self.commit_head,"w")
        # f_commit_head.write(curr_head)




    def restore(self):
        path_var="GitTest/f2/f3/f1a2.txt"
        if os.path.exists(path_var):
            print("yes exists")
        else:
            dir=os.path.exists(path_var[0:path_var.rfind('/')])
            print(os.path.exists(path_var[0:path_var.rfind('/')]))
            file_name=path_var[path_var.rfind('/')+1:]
            print(file_name)
            if os.path.exists(path_var[0:path_var.rfind('/')]):
                print("directory exists")
            else:
                os.mkdir(dir)
            f=open(path_var,"w").close()


    def pull(self):
        pass

    def push(self):
        pass

    def rollback(self):
        pass

    def diff(self):
        pass

