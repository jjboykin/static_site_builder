import os
import shutil

def copy_static(src, dst):

    # delete all the contents of the destination directory
    if os.path.exists(dst):
        print(f"Deleting directory {dst}")
        shutil.rmtree(dst)

    # copy all files and subdirectories, nested files, etc, logging the path of each file you copy
    if os.path.exists(src):
        dir_list = os.listdir(src)
        print(f"Creating directory {dst}")
        os.mkdir(dst)
        for item in dir_list:
            if os.path.isfile(os.path.join(src,item)):
                print(f"Copying file {item} from {os.path.join(src,item)} to {os.path.join(dst,item)}")
                shutil.copy(os.path.join(src,item), os.path.join(dst,item))
            else:
                copy_static(os.path.join(src,item), os.path.join(dst,item))


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)