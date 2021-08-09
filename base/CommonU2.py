# !/usr/bin/env python
# coding: utf-8
# @project_name: autotest-device
# @user: QM1997
# @time: 2019/2/7 0:42
# @desc:
import platform
import sys
import site_package.uiautomator2 as U2
from PIL import Image
import os
from core import *
from core.var import VAR
from time import sleep
from settings import *


def paramSwitch(args):
    parame = args[0].strip()[1:-1]
    d = {}
    for item in parame.split(','):
        a, b = item.split('=')
        d[a.strip()] = eval(b)
    return d


def operatePermissionsWindows(self, MIUI_VERSION):
    if MIUI_VERSION == "MIUI11":
        check = True
        while check:
            for text in ["允许", "同意并", "确定", "继续", "同意"]:
                if self(className="android.widget.Button", textContains=text).click_exists(timeout=0.5):
                    continue
            if not self(className="android.widget.Button", resourceId="android:id/button1").exists(timeout=0.5):
                check = False
    elif MIUI_VERSION == "MIUI12":
        check = True
        while check:
            for text in ["允许", "同意并", "确定", "继续", "同意"]:
                if self(className="android.widget.Button", textContains=text).click_exists(timeout=0.5):
                    continue
            if not self(className="android.widget.Button", resourceId="android:id/button1").exists(timeout=0.5):
                check = False


# 获得未下载的免费主题、字体。主题、字体首页搜索‘免费’，循环检查找到未下载的免费资源
# I : 循环次数   *Element : 判定元素
def checkFreeThemeOrFont(self, I, *Element, target=""):
    check = True
    element = paramSwitch(Element)
    while check:
        for i in range(0, I):
            self(className="android.widget.ListView").child(className="android.widget.Image",instance=i).click_exists(timeout=10.0)
            sleep(1.0)
            if self(**element).exists(timeout=5.0):
                check = False
                return True
            else:
                self.press("back")
                sleep(1.0)
            if i == I:
                check = False
                break


#  上下滑动查找元素
#  当hide=False时，该方法只适用于'首页'/'分类'/'我的'页面查找元素。
def checkElementByXpathByScroll(self,start_Y,end_Y,xpath_Element,hide=True,num=30):
    check = True
    count = 0
    # element = paramSwitch(Element)
    while check:
        if self.xpath(xpath_Element).exists:
            if hide:
                # self.swipe(0.500, 0.700, 0.500, 0.600)
                sleep(1.0)
                check = False
                return not check
            else:
                Y1 = \
                self(resourceId="com.android.thememanager:id/nav_container", className="android.widget.LinearLayout",
                     instance=1).info['bounds']['top']
                Y2 = self.xpath(xpath_Element).all()[0].attrib
                if Y2 > Y1:
                    self.swipe(0.500, 0.800, 0.500, 0.600)
                    sleep(0.5)
                    check = False
                    return not check
                else:
                    check = False
                    return not check
        else:
            self.swipe(0.550, start_Y, 0.550, end_Y)
            sleep(0.5)
            count += 1
        if count >= num:
            # U2.log_print("滑动" + str(num) + "次后查找结果:页面未找到目标元素:" + str(xpath_Element))
            U2.logger.warning("滑动" + str(num) + "次后查找结果:页面未找到目标元素:" + str(xpath_Element))
            check = False
            return check

#  上下滑动查找元素
#  当hide=False时，该方法只适用于'首页'/'分类'/'我的'页面查找元素。
def checkElementByScroll(self,start_Y,end_Y,*Element,hide=True,num=30):
    # check = True
    # count = 0
    # element = paramSwitch(Element)
    # while check:
    #     ret = self(**element).exists(timeout=1.0)
    #     if ret:
    #         if not hide:
    #             Y1 = self(resourceId="com.android.thememanager:id/nav_container", className="android.widget.LinearLayout",
    #                         instance=1).info['bounds']['top']
    #             Y2 = self(**element).center()[1]
    #             if Y2 > Y1 and not hide:
    #                 self.swipe(0.500, 0.800, 0.500, 0.700)
    #                 sleep(0.5)
    #         return ret
    #     else:
    #         ret = False
    #     if ret:
    #         check = False
    #         U2.log_print('滑动查找结果:页面是否存在目标' + str(element) + ':' + str(ret))
    #         return True
    #     else:
    #         self.swipe(0.550,start_Y,0.550,end_Y)
    #         sleep(0.5)
    #         count+=1
    #     if count >= num:
    #         U2.log_print('滑动查找结果:页面是否存在目标' + str(element) +':' + str(ret))
    #         check = False
    #         return False
    check = True
    count = 0
    element = paramSwitch(Element)
    res = []
    while check:
        if self(**element).exists(timeout=1.0):
            if hide:
                self.swipe(0.500, 0.700, 0.500, 0.670)
                count += 1
                sleep(1.0)
                check = False
                res.append(not check)
                res.append(count)
                return res
            else:
                if self(resourceId="com.android.thememanager:id/nav_container",className="android.widget.LinearLayout",instance=1).exists():
                    Y1 = self(resourceId="com.android.thememanager:id/nav_container",className="android.widget.LinearLayout",instance=1).info['bounds']['top']
                    Y2 = self(**element).info['bounds']['bottom']
                    if Y2 > Y1:
                        self.swipe(0.500, 0.800, 0.500, 0.600)
                        count += 1
                        sleep(1.0)
                        check = False
                        res.append(not check)
                        res.append(count)
                        return res
                    else:
                        check = False
                        res.append(not check)
                        res.append(count)
                        return res
                else:
                    check = False
                    res.append(not check)
                    res.append(count)
                    return res
        else:
            self.swipe(0.550, start_Y, 0.550, end_Y)
            sleep(1.0)
            count += 1
        if count >= num:
            # U2.log_print("滑动"+str(num)+"次后查找结果:页面未找到目标元素:" + str(element))
            U2.logger.warning("滑动"+str(num)+"次后查找结果:页面未找到目标元素:" + str(element))
            check = False
    if count >= num:
        res.append(check)
        res.append(count)
        return res
    else:
        res.append(not check)
        res.append(count)
        return res


# 左右滑动查找元素
def checkElementByScroll2(self,start_X,end_X,common_Y,*Element,num=10):
    check = True
    count = 0
    element = paramSwitch(Element)
    sleep(1.0)
    while check:
        ret = self(**element).exists(timeout=2.0)
        if ret:
            check = False
            # U2.log_print('滑动查找结果:页面是否存在目标' + str(element) + ':' + str(ret))
            U2.logger.warning('滑动查找结果:页面是否存在目标' + str(element) + ':' + str(ret))
            return not check
        else:
            self.swipe(start_X,common_Y,end_X,common_Y)
            sleep(1.0)
            count += 1
        if count >= num:
            # U2.log_print('滑动查找结果:页面是否存在目标' + str(element) +':' + str(ret))
            U2.logger.warning('滑动查找结果:页面是否存在目标' + str(element) +':' + str(ret))
            check = False
            return check

# 从推荐页寻找并进入某一收费资源详情页 category = '主题' '字体' 字体资源只能从推荐页进入
# 先进入'主题'页，是从主题页寻找并进入某一收费资源详情页
# def getChargeThemePage2(self):
#     check = True
#     while check:
#         sleep(0.5)
#         if self(resou)
#         count = self(resourceId="com.android.thememanager:id/container", className="android.widget.LinearLayout").count
#         for i in range(0, count):
#             self(resourceId="com.android.thememanager:id/container", className="android.widget.LinearLayout", instance=i).click()
#             if self(resourceId="com.android.thememanager:id/downloadBtn").get_text(timeout=10.0) == '购买':
#                 check = True
#                 break
#             else:
#                 self.press('back')
#                 sleep(1.0)
#         else:
#             self.swipe(0.500, 0.800, 0.500, 0.400)
#             sleep(1.0)

# 先进入'主题'页，是从主题页寻找并进入某一收费资源详情页
def getChargeThemePage2(self, start_Y,end_Y,num=30):
    check = True
    count = 0
    while check:
        sleep(0.5)
        if self(resourceId="com.android.thememanager:id/text_switcher").exists():
            Y1 = self(resourceId="com.android.thememanager:id/nav_container", className="android.widget.LinearLayout",
                      instance=1).info['bounds']['top']
            Y2 = self(resourceId="com.android.thememanager:id/text_switcher").center()[1]
            if Y2 < Y1:
                x = self(resourceId="com.android.thememanager:id/text_switcher").center()[0]
                self.click(x, Y2 - 100)
                check=False
            else:
                self.swipe(0.500,0.700,0.500,0.500)
                sleep(0.5)
                x = self(resourceId="com.android.thememanager:id/text_switcher").center()[0]
                Y3 = self(resourceId="com.android.thememanager:id/text_switcher").center()[1]
                self.click(x, Y3 - 100)
                check = False
        else:
            self.swipe(0.500, start_Y, 0.500, end_Y)
            count += 1
            sleep(1.0)
        if count > num:
            check = False

def getChargeThemePage(self,category):
    check = False
    while not check:
        count = self(resourceId="com.android.thememanager:id/price").count
        Y1 = self(resourceId="com.android.thememanager:id/nav_container", className="android.widget.LinearLayout",
                    instance=1).info['bounds']['top']
        for i in range(0, count):
            Y2 = self(resourceId="com.android.thememanager:id/price", instance=i).center()[1]
            if Y1 > Y2:
                # self(resourceId="com.android.thememanager:id/price", instance=i).click()
                (x, y) = self(resourceId="com.android.thememanager:id/price").center()
                self.click(x, y - 300)
                if self(resourceId="com.android.thememanager:id/price").get_text(timeout=10.0) != '免费':
                    check = True
                    break
                else:
                    self.press('back')
                    sleep(1.0)
        else:
            self.swipe(0.500, 0.800, 0.500, 0.400)
            sleep(1.0)

# def checkElementByScrollAndClick(self,start_Y,end_Y,*Element,num=30):
#     check = False
#     count = 0
#     arg_list = []
#     for arg in Element:
#         element = paramSwitch(arg)
#         arg_list.append(element)
#     sleep(2.0)
#     while not check:
#         ret = self(**arg_list[0]).exists()
#         if ret:
#             self(**arg_list[0]).click()
#             if self(**arg_list[1]).get_text() != '免费':


def getCurrentApp_package(sn):
    if platform.system() == "Windows":
        a = os.popen("adb -s " + sn + " shell dumpsys window | findstr mCurrentFocus").readline()
        e = a.split('u0 ')[1].rstrip().rstrip('}').split('/')
    else:
        a = os.popen("adb -s " + sn + " shell dumpsys window | grep mCurrentFocus").readline()
        e = a.split('u0 ')[1].rstrip().rstrip('}').split('/')
    return e[0]


def getCurrentApp_activity(sn):
    if platform.system() == "Windows":
        a = os.popen("adb -s " + sn + " shell dumpsys window | findstr mCurrentFocus").readline()
        e = a.split('u0 ')[1].rstrip().rstrip('}').split('/')
    else:
        a = os.popen("adb -s " + sn + " shell dumpsys window | grep mCurrentFocus").readline()
        e = a.split('u0 ')[1].rstrip().rstrip('}').split('/')
    return e[1]


# 异常时记录截图
def get_screenshot(self, path, image_name):
    if VAR.mode == 1:
        if os.path.exists(path):
            if platform.system() == "Windows":
                root = path + "\\" + image_name
            else:
                root = path + "/" + image_name
            self.screenshot(filename=root)
            pic = Image.open(root).resize((270, 520), Image.ANTIALIAS)  # 和原始像素比例1080*2280压缩一倍
            pic.save(root)
            self.log.debug(root, img_path=True)
        else:
            CheckPoint("Error screenshot, please check img_path")

    # if os.path.exists(path):
    #     root = path + "\\" + image_name
    #     self.screenshot(filename=root)
    #     pic = Image.open(root).resize((540, 1140), Image.ANTIALIAS) # 和原始像素比例1080*2280压缩一倍
    #     pic.save(root)
    # else:
    #     if VAR.mode == 1:
    #         CheckPoint("Error screenshot, please check path")


# 通过坐标点获取该点的颜色值
def get_color(self, x, y):
    path_img1 = os.path.dirname(sys.path[0])+"\\disposable\\template.png"
    self.screenshot(path_img1)
    sleep(1.0)
    # img_src = Image.open(path_img1)
    img_src = Image.open(path_img1).convert('RGB')
    str_strlist = img_src.convert('RGB').load()
    RGB = str_strlist[x, y]
    img_src.close()
    # os.remove(path_img1)
    return RGB


def checkElementByScrollForDisapear(self, start_Y, end_Y, *Element, num=30):
    check = True
    count = 0
    element = paramSwitch(Element)
    res = []
    while check:
        if not self(**element).exists(timeout=1.0):
            check = False
            res.append(not check)
            res.append(count)
            return res
            # if hide:
            #     self.swipe(0.500, 0.700, 0.500, 0.650)
            #     sleep(1.0)
            #     check = False
            #     return not check
            # else:
            #     if self(resourceId="com.android.thememanager:id/nav_container", className="android.widget.LinearLayout", instance=1).exists():
            #         Y1 = self(resourceId="com.android.thememanager:id/nav_container", className="android.widget.LinearLayout", instance=1).info['bounds']['top']
            #         Y2 = self(**element).info['bounds']['bottom']
            #         if Y2 > Y1:
            #             self.swipe(0.500, 0.800, 0.500, 0.600)
            #             sleep(1.0)
            #             check=False
            #             res.append(not check)
            #             res.append(count)
            #             return res
            #         else:
            #             check = False
            #             res.append(not check)
            #             res.append(count)
            #             return not check
            #     else:
            #         check = False
            #         res.append(not check)
            #         res.append(count)
            #         return res
        else:
            self.swipe(0.550, start_Y, 0.550, end_Y)
            sleep(1.0)
            count+=1
        if count >= num:
            U2.log_print("滑动"+str(num)+"次后查找结果:页面未找到目标元素:" + str(element))
            check = False
            res.append(check)
            res.append(count)
            return res


def assert_self2(self, type, normal_msg, fail_Msg,*args):
    if type == "assertTrue":
        if self.assertTrue(args[0],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertEqual":
        if self.assertEqual(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertNotEqual":
        if self.assertNotEqual(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertIn":
        if self.assertIn(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertNotIn":
        if self.assertNotIn(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertIs":
        if self.assertIs(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertLess":
        if self.assertLess(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertLessEqual":
        if self.assertLessEqual(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertGreater":
        if self.assertGreater(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertGreaterEqual":
        if self.assertGreaterEqual(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
    elif type == "assertIsNone":
        if self.assertIsNone(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False
    elif type == "assertIsNotNone":
        if self.assertIsNotNone(args[0],args[1],fail_Msg):
            CheckPoint(normal_msg)
        else:
            return False


# 小米画报业务API
def start_wallpaper_app(self, sn):
    os.system("adb -s " + sn + " shell am start -n " + config.pkg_activity_wallPaper)
    sleep(1.0)
    self(text='正在加载...').wait_gone(timeout=20.0)
