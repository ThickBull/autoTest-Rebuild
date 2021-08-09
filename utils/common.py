# !/usr/bin/env python
# coding: utf-8
# @project_name: autoTest-new
# @user: QM1997
# @time: 2019/4/26 10:23
# @desc:

import os
import sys
import importlib
import traceback

__all__ = ["path_join", "make_dirs", "get_all_files", "import_module"]


def path_join(*args):
    return os.path.join(*args)


def make_dirs(path):
    os.makedirs(path, exist_ok=True)


def get_all_files(dirname, target=""):
    """返回dir文件夹下的所有的文件的路径"""
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        file_name_list.sort(key=lambda x: x.split('.py')[0])
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if apath.endswith(".py") and "__" not in apath and target in apath:
                result.append(apath)
    return result


def import_module(module_path):
    if not os.path.exists(module_path):
        raise Exception("module path not exists")
    dirname, filename = os.path.split(module_path)
    sys.path.insert(0, dirname)
    filename = filename[:-3]
    try:
        module = importlib.import_module(filename)
        sys.path.pop(0)
        return module
    except ImportError as e:
        traceback.print_exc()
        raise Exception("Module Can Not Import:{}".format(module_path))