# -*- coding:utf-8 -*-
"""
@Title:[铃声]试听铃声
@Desc:
@Step:
@Author:qm
@Date Created:2019/4/15 15:42
@project_name:autotest-device
"""
from base import CommonU2
from core.testcase import TestCase
from core import CheckPoint
from core import Step
from settings import *
from time import sleep


class Bell_P4_C3361157(TestCase):

    def setUp(self):
        print("ok")
        self.d.session(config.package, launch_timeout=10)

    def test_step(self):
        Step("Step.1.铃声在线列表页，点击某个资源")
        self.d(className="android.widget.RelativeLayout", description=u"铃声").click(timeout=5.0)
        self.d(resourceId="com.android.thememanager:id/name").click()
        check1 = True if self.d(resourceId="com.android.thememanager:id/name").sibling(
                resourceId="com.android.thememanager:id/audio_playing").exists(timeout=10.0) else False
        if self.assertTrue(check1, "异常1.点击某个资源，播放标识是否显示:False"):
            CheckPoint("正常1.点击某个资源，播放标识是否显示:True")
            Step("Step.2.在播放的过程中，再次点击资源；或者播放完成后查看界面")
            self.d(resourceId="com.android.thememanager:id/name").click()
            check2 = True if not self.d(resourceId="com.android.thememanager:id/name").sibling(
                resourceId="com.android.thememanager:id/audio_playing").exists(timeout=2.0) else False
            if self.assertTrue(check2, "异常2.再次点击某个资源，播放标识是否消失:False"):
                CheckPoint("正常2.再次点击某个资源，播放标识是否消失:True")
        if not self.d(resourceId="com.android.thememanager:id/audio_playing").exists(timeout=1.0):
            self.d(resourceId="com.android.thememanager:id/name").click()
            if self.assertTrue(self.d(resourceId="com.android.thememanager:id/audio_playing").wait_gone(timeout=120.0),
                               "异常3.等待铃声播放完毕，播放标识是否消失:False"):
                CheckPoint("正常3.等待铃声播放完毕，播放标识是否消失:True")

    def tearDown(self):
        print("ok2")
        self.d.app_stop(config.package)
