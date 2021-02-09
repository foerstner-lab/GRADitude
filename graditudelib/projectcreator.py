import os
import sys
import pandas as pd


def create_root_folder(project_name):
    """Create the root folder of a new project with the given name.

    Arguments:
    - `project_name`: Name of the project root folder
    """
    if not os.path.exists(project_name):
        os.mkdir(project_name)
    else:
        sys.stderr.write("Cannot create folder \"%s\"! File/folder with "
                         "the same name exists already.\n" % project_name)
        sys.exit(2)


def create_subfolders(root, subfolders):
    """Create required subfolders in the given folder.

    Arguments:
    - `project_name`: Name of the project root folder
    """
    for folder in subfolders:
        if not os.path.exists(root + "/" + folder):
            os.mkdir(root + "/" + folder)


def create_version_file(version_file_path, version):
    with open(version_file_path, "w") as fh:
        fh.write("GRADitude version: %s\n" % version)
        fh.write("Python version: %s\n" % sys.version.replace("\n", " "))
        fh.write("pandas version: %s\n" % pd.__version__)

