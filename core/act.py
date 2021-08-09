# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : act.py
@Software: PyCharm
@Time    : 2019/12/17 16:46
@Author  : qm
@Email   : quming5@xiaomi.com
@desc    :
"""


import os
import sys
from time import sleep
from multiprocessing import Pool
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.var import VAR
from core.helper import get_tests
from site_package.uiautomator2 import connect
from site_package import unittest
from core.runner import TextTestRunner
from core.log import logger
from core.report import generate_task_report
# from site_package.unittest.runner import TextTestRunner


def initialize(name, sn):
    try:
        d = connect(sn)  # d 是UIAutomatorServer对象
        # d.debug = True
        # setattr(d, "click_post_delay", 0.5)  # 点击时间间隔
        d.settings["operation_delay"] = (0.25, 0.25)
        logger.debug("device_MIUI11 info:{}".format(d.info))
        setattr(VAR, "d", d)
        setattr(VAR, "name", name)
        setattr(VAR, "sn", sn)
    except Exception:
        raise Exception("请查看手机的sn是否配置正确")


def run_process(name, sn):
    initialize(name, sn)
    tests = get_tests()
    suite = unittest.TestSuite(tests)
    runner = TextTestRunner(descriptions='task({}) for {}'.format(VAR.project_start_time, name))
    result = runner.run(suite)  # result: <core.runner.TextTestResult run=3 errors=2 failures=0>
    result.log = logger
    sleep(3.0)
    generate_task_report(name, result)


if __name__ == '__main__':
    VERSION = "1.2.0"
    logger.info("--------------------- Operate Test Version：{} --------------------".format(VERSION))
    if VAR.mode == 1:
        logger.info("Execute in Debug Mode=1")
    elif VAR.mode == 2:
        logger.info("Execute in Debug Mode=2")
    elif VAR.mode == 3:
        logger.info("Execute in Debug Mode=3")
    device_dict = getattr(VAR, "device_dict")
    if len(device_dict) == 1:
        (NAME, SN), = device_dict.items()
        Name = NAME + "_" + SN
        # UI_VERSION = os.popen("adb -s " + SN + " shell getprop ro.miui.ui.version.name").read().strip()
        run_process(Name, SN)
    else:
        p = Pool(processes=len(device_dict))  # VAR.sn['config']  VAR.config['sn']
        for NAME, SN in device_dict.items():
            Name = NAME + "_" + SN
            # UI_VERSION = os.popen("adb -s " + SN + " shell getprop ro.miui.ui.version.name").read().strip()
            p.apply_async(run_process, args=(Name, SN))  # apply_async 子进程并行执行 apply 子进程串行执行
        p.close()
        p.join()
