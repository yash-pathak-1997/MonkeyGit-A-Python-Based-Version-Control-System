import hashlib
import os
import pathlib
path="/home/krati/GitTest"
def filepath(path,ls):
    relative = pathlib.Path(os.path.relpath(path))
    for p in pathlib.Path(relative).iterdir():
        if p.is_file():
            sha=hash_calc(p)
            # ls.append(p)
            print("file name", str(p).replace("../",""),"sha= ",sha)
        elif ((p.is_dir()) & (not p.match(".git-vcs"))):
           #print("directory", p)
            filepath(p,ls)


def hash_calc(filename):
    sha256_hash=hashlib.sha256()
    fopen=open(filename,"rb")
    for byte_block in iter(lambda:fopen.read(4096),b""):
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

ls=[]
filepath(path,ls)
print(ls)

