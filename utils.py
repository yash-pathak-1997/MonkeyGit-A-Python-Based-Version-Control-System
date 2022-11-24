import os
import pathlib
import hashlib
import pandas as pd
from Config import UnTrackedDel,UnTrackedMod,UnTrackedNew,TrackedDel,TrackedMod,TrackedNew


def filepath(path, files_list, sha_list, file_track):
    relative = pathlib.Path(os.path.relpath(path))
    for p in pathlib.Path(relative).iterdir():
        if p.is_file():
            files_list.append(str(p).replace("../", ""))
            sha_list.append(hash_calc(p))
            file_track.append(UnTrackedNew)
        elif (p.is_dir()) & (not p.match(".git-vcs")):
            filepath(p, files_list, sha_list, file_track)


def hash_calc(filename):
    sha256_hash = hashlib.sha256()
    fopen = open(filename, "rb")
    for byte_block in iter(lambda: fopen.read(4096), b""):
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def create_df(files_list, sha_list, track_flag):
    df = pd.DataFrame()
    df['filename'] = files_list
    df['sha'] = sha_list
    df['track_flag'] = track_flag
    return df


# checking only modify file and delete file and add new file
def update_repo_info(csv_path, repo_path, file_list, sha_list, track_flag):
    new_file_list = list()
    new_sha_list = list()
    new_track_flag = list()
    print(file_list, sha_list, track_flag)
    filepath(repo_path, new_file_list, new_sha_list, new_track_flag)

    # check add new file
    for i in new_file_list:
        if i not in file_list:
            file_list.append(i)
            sha_list.append(hash_calc(i))
            track_flag.append(UnTrackedNew)

    # check delete file
    del_list = list()
    for i in range(0, len(file_list)):
        if file_list[i] not in new_file_list:
            if track_flag[i] in [UnTrackedNew, UnTrackedMod, UnTrackedDel]:
                del_list.append(i)

            elif track_flag[i] in [TrackedNew, TrackedMod, TrackedDel]:
                file_list.append(i)
                sha_list.append(None)
                track_flag.append(UnTrackedDel)

    # check modify file
    for i in range(0, len(file_list)):
        print("enyter")
        if sha_list[i] != new_sha_list[i]:
            if track_flag[i] in [UnTrackedNew, UnTrackedMod, UnTrackedDel]:
                sha_list[i] = hash_calc(file_list[i])

            elif track_flag[i] in [TrackedNew, TrackedMod, TrackedDel]:
                file_list.append(file_list[i])
                sha_list.append(hash_calc(file_list[i]))
                track_flag.append(UnTrackedMod)
