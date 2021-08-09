# !/usr/bin/env python
# coding: utf-8
# @project_name: autoTest-new
# @user: QM1997
# @time: 2019/4/26 0:17
# @desc:

from site_package import unittest
import os
from core.var import VAR
from core.log import logger
import settings
import utils


__all__ = ["get_tests"]


def get_tests():
    tests = []
    scripts = []
    if VAR.mode == 1:
        scripts = get_scripts()
    elif VAR.mode == 2:
        with open(os.path.join(settings.BASE_DIR, "scripts", "scripts"), "r", encoding="utf-8") as f:
            scripts = [f.read(), ]
    elif VAR.mode == 3:
        scripts = [os.path.join(settings.BASE_DIR, "scripts", "Temp.py"), ]
    loader = unittest.TestLoader()
    for script in scripts:
        module = utils.import_module(script)
        file_name = os.path.basename(script)[:-3]
        # print("module:", module)
        # print("file_name:", file_name)
        obj = getattr(module, file_name, None)
        # print("obj:", obj)
        if not obj:
            raise Exception("在测试用例：{}中未获取到测试类：{},测试类名需和测试用例名保持一致".format(script, file_name))
        if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            tests.append(loader.loadTestsFromTestCase(obj))
        else:
            raise Exception("测试用例：{}中的测试类：{}不是TestCase的子类，请继承TestCase".format(script, file_name))
    return tests


def get_scripts():
    scripts = []
    if settings.Var["level"] == "":
        for k in VAR.scripts_module.split(","):
            scripts_dir = os.path.join(settings.BASE_DIR, "scripts", settings.Var['scripts_dir'], k)
            if not os.path.exists(scripts_dir):
                raise Exception("{} 目标路径不存在,请查看配置文件scripts_module_miui节点是否配置正确.".format(scripts_dir))
            scripts += utils.get_all_files(scripts_dir)
        logger.info("本次任务共计执行 " + str(len(scripts)) + " 条用例")
        return scripts
    else:
        case_level = settings.Var["level"]
        for k in VAR.scripts_module.split(","):
            scripts_dir = os.path.join(settings.BASE_DIR, "scripts", settings.Var['scripts_dir'], k)
            if not os.path.exists(scripts_dir):
                raise Exception("{} 目标路径不存在,请查看配置文件scripts_module_miui节点是否配置正确.".format(scripts_dir))
            scripts += utils.get_all_files(scripts_dir, case_level)
        logger.info("本次任务共计执行 " + str(len(scripts)) + " 条用例")
        return scripts

