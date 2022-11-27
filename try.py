import shutil

src_path ="/home/krati/Documents/AOS-Project/AOS-project/AOS-Project-VCS/GitTest"
dst_path = "/home/krati/Downloads/new"
shutil.copytree(src_path, dst_path,dirs_exist_ok=True)
print('Copied')