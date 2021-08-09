# -*- encoding: utf-8 -*-
"""
@File    : settings.py
@Project : autoText-rebuild
@Time    : 2019/12/17 17:47
@Author  : qm
@Email   :
@desc    :
"""


import os

"""

"""


Var = {
    "report_folder": "report",
    "scripts_dir": "test1",
    "scripts_module": "test2",
    "level": "",
    "receiver": "quming5@XXX.com,v-wangruichao@XXX.com,v-libo1@XXX.com"
}

LOG = {
    "console_level": "INFO",  # DEBUG
    "file_level": "INFO",  # INFO
    "console_pattern": "%(asctime)s  %(levelname)s : %(message)s",
    "file_pattern": "%(asctime)s  %(name)s  %(levelname)s : %(message)s",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # return 项目根路径

CONTENT = """
import random
from base import CommonU2
from core.testcase import TestCase
from core import CheckPoint
from core import Step
from settings import *
from time import sleep


class Temp(TestCase):

    def setUp(self):
        pass

    def test(self):
{{ content }}

    def tearDown(self):
        pass

"""
# import platform
# print(platform.system())  # 油半途  返回Linux  mac 返回 Darwin


class Config:
    package = "com.android.xxx"
    setting_package = "com.android.xxx"
    pkg_activity_wallPaper = "com.mfashiongallery.emag/.app.main.AppMainActivity"
    pkg_wallPaper = "com.mfashiongallery.emag"
    account = "2246397792"
    password = "xiaomi0123"


config = Config()

