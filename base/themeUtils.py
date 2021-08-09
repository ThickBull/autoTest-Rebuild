# -*- coding: utf-8 -*-
"""
@Desc: TODO
@File : themeUtils.py
@Project: autoTest-rebuild
@Author : qm
@Time : 2020/3/18 10:05 上午
"""
"""
1, 当有下载资源成功时，teardown步骤中加入清除通知操作
self.d.open_notification()
self.d(resourceId='com.android.systemui:id/dismiss_view').click_exists(timeout=2)

2，清除本地第三方字体
os.system("adb -s " + self.sn + " shell rm -rf /sdcard/MIUI/theme/.data/content/fonts/*")

3，python脚本代码读取手机存储路径下的文件
res = os.popen("adb shell \"cd /storage/emulated/0/MIUI && cd .wallpaper && ls\"").read()
print(res)

4,
"""

