import os
import shutil
def rm_public(dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)

def copy(src, dst):
    os.mkdir(dst)
    dir_list = os.listdir(src)
    for file in dir_list:
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy(src_path, dst_path)
