# -*- coding: utf-8 -*-
"""
@Desc: TODO
@File : wda_ios.py
@Project: autoTest-rebuild 
@Author : qm
@Time : 2020/8/10 5:36 下午
"""

import wda
from time import sleep

bundle_id = 'com.netease.cloudmusic'
driver = wda.Client('http://10.234.212.231:8100')
s = driver.session('com.apple.Preferences')
# sleep(5)
# s(text=u'通用').tap()
# s(text=u'关于本机').tap()
a = s.session_id(driver)
print(a)
print("OK1")
# 点击home button
# s.home()


# if __name__ == '__main__':
#     import os
#     deviceName,platformVersion,udid = 0,0,0
#     deviceUdid = os.popen('system_profiler SPUSBDataType | grep "Serial Number:.*" | sed s#".*Serial Number: "##').readlines()
#     print(deviceUdid)


