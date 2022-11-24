import os
import pathlib


def filepath(path, files_list):
    relative = pathlib.Path(os.path.relpath(path))
    for p in pathlib.Path(relative).iterdir():
        if p.is_file():
            files_list.append(str(p).replace("../", ""))
        elif (p.is_dir()) & (not p.match(".git-vcs")):
            filepath(p, files_list)
