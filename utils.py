import os
import pathlib
import hashlib

import pandas as pd


def filepath(path, files_list,sha_list,file_track):
    relative = pathlib.Path(os.path.relpath(path))
    for p in pathlib.Path(relative).iterdir():
        if p.is_file():
            files_list.append(str(p).replace("../", ""))
            sha_list.append(hash_calc(p))
            file_track.append(0)
        elif (p.is_dir()) & (not p.match(".git-vcs")):
            filepath(p, files_list,sha_list,file_track)


def hash_calc(filename):
    sha256_hash=hashlib.sha256()
    fopen=open(filename,"rb")
    for byte_block in iter(lambda:fopen.read(4096),b""):
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def create_df(files_list,sha_list,track_flag):
    df = pd.DataFrame()
    df['filename'] = files_list
    df['sha'] = sha_list
    df['track_flag'] = track_flag
    return df


def update_repo_info(csv_path,repo_path,file_list,sha_list,track_flag):
    filepath(repo_path,file_list,sha_list,track_flag)
    df_new=create_df(file_list,sha_list,track_flag)
    df=pd.read_csv(csv_path)

    print(df_new)
    print("......................")
    print(df)

