# !/usr/bin/env python
# coding: utf-8
# @project_name: autoTest-new
# @user: QM1997
# @time: 2019/4/26 19:33
# @desc:

import contextlib
from site_package import unittest
import platform
import sys
import os
import re
import time
import datetime
from PIL import Image
from core.log import Logger
from core.var import VAR
from core.report import generate_case_report


__all__ = ["TestCase"]


class SkipTest(Exception):
    """
    Raise this exception in a test to skip it.

    Usually you can use TestCase.skipTest() or one of the skipping decorators
    instead of raising this directly.
    """


class _ShouldStop(Exception):
    """
    The test should stop.
    """


class _Outcome(object):

    def __init__(self, result=None):
        self.expecting_failure = False
        self.result = result
        self.result_supports_subtests = hasattr(result, "addSubTest")
        self.success = True
        self.skipped = []
        self.expectedFailure = None
        self.errors = []

    # add by QM
    @property
    def testResult(self):
        if self.success:
            return "pass"
        for test, exc_info in self.errors:
            if exc_info is not None:
                if issubclass(exc_info[0], AssertionError):
                    return "fail"
                else:
                    return "error"

    @contextlib.contextmanager
    def testPartExecutor(self, test_case, isTest=False):
        old_success = self.success
        self.success = True
        try:
            yield
        except KeyboardInterrupt:
            raise
        except SkipTest as e:
            self.success = False
            self.skipped.append((test_case, str(e)))
        except _ShouldStop:
            pass
        except:
            exc_info = sys.exc_info()
            if self.expecting_failure:
                self.expectedFailure = exc_info
            else:
                self.success = False
                self.errors.append((test_case, exc_info))
            # explicitly break a reference cycle:
            # exc_info -> frame -> exc_info
            exc_info = None
        else:
            if self.result_supports_subtests and self.success:
                self.errors.append((test_case, None))
        finally:
            self.success = self.success and old_success


failed = 0


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.init()

    def init(self):
        self.case_name = self.__class__.__name__
        self.log = Logger.get_logger(self.case_name)
        self.d = getattr(VAR, "d")
        self.name = getattr(VAR, "name")
        self.sn = getattr(VAR, "sn")
        setattr(self.d, "log", self.log)
        self.startTime = datetime.datetime.now()
        VAR.cur_case_name = self.case_name
        s = sys.modules[self.__module__]
        self.log.info(s.__file__, file_path=True)
        self.parse_doc(s.__doc__)
        self.add_sn()
        for caseReport in VAR.report_dir_list:
            if self.name in caseReport:
                self.caseReport_dir = os.path.join(caseReport, self.case_name)
                self.screen_shot_dir = os.path.join(self.caseReport_dir, "image")
                if VAR.mode == 1:
                    os.makedirs(self.caseReport_dir, exist_ok=True)
                    os.makedirs(self.screen_shot_dir, exist_ok=True)

    # by QM
    def screenshot_get(self):
        if VAR.mode == 1:
            if os.path.exists(self.screen_shot_dir):
                if platform.system() == "Windows":
                    root = self.screen_shot_dir + "\\" + time.strftime('%Y-%m-%d-%H-%M-%S',
                                                        time.localtime(time.time())) + ".png"
                else:
                    root = self.screen_shot_dir + "/" + time.strftime('%Y-%m-%d-%H-%M-%S',
                                                                       time.localtime(time.time())) + ".png"
                self.d.screenshot(filename=root)
                pic = Image.open(root).resize((270, 520), Image.ANTIALIAS)  # 和原始像素比例1080*2280压缩一倍
                pic.save(root)
                self.log.debug(root, img_path=True)
        else:
            self.log.error("Error screenshot, please check path")

    def run(self, result=None):
        self.init()
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
                getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, self, skip_why)
            finally:
                result.stopTest(self)
            return
        expecting_failure_method = getattr(testMethod,"__unittest_expecting_failure__", False)
        expecting_failure_class = getattr(self,"__unittest_expecting_failure__", False)
        expecting_failure = expecting_failure_class or expecting_failure_method
        outcome = _Outcome(result)
        try:
            self._outcome = outcome
            with outcome.testPartExecutor(self):
                try:
                    self.log.info("--------------- {} setUp start ---------------".format(
                        self.case_name), setUp_start=True)
                    self.setUp()
                    time.sleep(0.5)
                    self.log.info(
                        "--------------- {} setUp end ---------------".format(
                            self.case_name), setUp_end=True)
                except Exception as e:
                    self.log.exception(e)
                    time.sleep(0.5)
                    self.log.error(
                        "--------------- {} setUp end ---------------".format(self.case_name), setUp_end=True)
                    raise e
            time.sleep(0.5)
            if outcome.success:
                outcome.expecting_failure = expecting_failure
                with outcome.testPartExecutor(self, isTest=True):
                    try:
                        self.log.info(
                            "--------------- {} test start ---------------".format(
                                self.case_name), test_start=True)
                        testMethod()
                        time.sleep(0.5)
                        self.log.info(
                            "--------------- {} test end ---------------".format(
                                self.case_name), test_end=True)
                    except Exception as e:
                        self.log.exception(e)
                        time.sleep(0.5)
                        self.log.error(
                            "--------------- {} test end ---------------".format(
                                self.case_name), test_end=True)
                        raise e
                time.sleep(1.0)
                with outcome.testPartExecutor(self):
                    try:
                        self.log.info(
                            "--------------- {} tearDown start ---------------".format(
                                self.case_name), tearDown_start=True)
                        self.tearDown()
                        time.sleep(0.5)
                        self.log.info(
                            "--------------- {} tearDown end ---------------".format(
                                self.case_name), tearDown_end=True)
                    except Exception as e:
                        self.log.exception(e)
                        time.sleep(0.5)
                        self.log.error(
                            "--------------- {} tearDown end ---------------".format(
                                self.case_name), tearDown_end=True)
                        raise e
            self.doCleanups()
            for test, reason in outcome.skipped:
                self._addSkip(result, test, reason)
            self._feedErrorsToResult(result, outcome.errors)
            # if outcome.success:
            #     if expecting_failure:
            #         if outcome.expectedFailure:
            #             self._addExpectedFailure(result, outcome.expectedFailure)
            #         else:
            #             self._addUnexpectedSuccess(result)
            #     else:
            #         result.addSuccess(self)
            # 加入 failed retry 功能
            if outcome.success:
                if expecting_failure:
                    if outcome.expectedFailure:
                        self._addExpectedFailure(result, outcome.expectedFailure)
                    else:
                        self._addUnexpectedSuccess(result)
                else:
                    result.addSuccess(self)
            elif VAR.mode == 1:
                self.log.info("========== failed retry once =========")
                time.sleep(1.0)
                # outcome.success置为true重新运行case
                outcome.success = True
                with outcome.testPartExecutor(self):
                    try:
                        self.log.info("--------------- {} setUp start ---------------".format(
                                self.case_name), setUp_start=True)
                        self.setUp()
                        time.sleep(0.5)
                        self.log.info(
                            "--------------- {} setUp end ---------------".format(
                                self.case_name), setUp_end=True)
                    except Exception as e:
                        self.log.exception(e)
                        self.screenshot_get()  # 第二遍setUp异常截图
                        time.sleep(0.5)
                        self.log.error(
                            "--------------- {} setUp end ---------------".format(self.case_name), setUp_end=True)
                        raise e
                time.sleep(0.5)
                if outcome.success:
                    outcome.expecting_failure = expecting_failure
                    with outcome.testPartExecutor(self, isTest=True):
                        try:
                            self.log.info(
                                "--------------- {} test start ---------------".format(
                                    self.case_name), test_start=True)
                            testMethod()
                            time.sleep(0.5)
                            self.log.info(
                                "--------------- {} test end ---------------".format(
                                    self.case_name), test_end=True)
                        except Exception as e:
                            self.log.exception(e)
                            self.screenshot_get()  # 第二遍testMethod异常截图
                            time.sleep(0.5)
                            self.log.error(
                                "--------------- {} test end ---------------".format(
                                    self.case_name), test_end=True)
                            raise e
                    time.sleep(0.5)
                    with outcome.testPartExecutor(self):
                        try:
                            self.log.info(
                                "--------------- {} tearDown start ---------------".format(
                                    self.case_name), tearDown_start=True)
                            self.tearDown()
                            time.sleep(0.5)
                            self.log.info(
                                "--------------- {} tearDown end ---------------".format(
                                    self.case_name), tearDown_end=True)
                        except Exception as e:
                            self.log.exception(e)
                            self.screenshot_get()  # 第二遍tearDown异常截图
                            time.sleep(0.5)
                            self.log.error(
                                "--------------- {} tearDown end ---------------".format(
                                    self.case_name), tearDown_end=True)
                            raise e
                time.sleep(0.5)
                self.doCleanups()
                for test, reason in outcome.skipped:
                    self._addSkip(result, test, reason)
                self._feedErrorsToResult(result, outcome.errors)
                if outcome.success:
                    if expecting_failure:
                        if outcome.expectedFailure:
                            self._addExpectedFailure(result, outcome.expectedFailure)
                        else:
                            self._addUnexpectedSuccess(result)
                    else:
                        result.addSuccess(self)
            if outcome.testResult == "pass":
                self.log.info(
                    "--------------- TestCase {} PASS ---------------".format(
                        self.case_name), teseCase_end=True)
            else:
                global failed
                failed += 1
                self.log.error(
                    "--------------- TestCase {} {} ---------------".format(
                        self.case_name, outcome.testResult.upper()), teseCase_end=True)
            self.collect_something(outcome, result)
            result.testCases.append(self)  # add by yang
            generate_case_report(self, self.name, VAR.report_dir_list)
            setattr(VAR, "failed", failed)
            return result
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            # explicitly break reference cycles:
            # outcome.errors -> frame -> outcome -> outcome.errors
            # outcome.expectedFailure -> frame -> outcome -> outcome.expectedFailure
            outcome.errors.clear()
            outcome.expectedFailure = None
            # clear the outcome, no more needed
            self._outcome = None

    # ----add begin----
    def collect_something(self, outcome, result):
        self.stopTime = datetime.datetime.now()
        self.testResult = outcome.testResult
        self.timeTaken = result.getTimeTaken(self.stopTime, self.startTime)
        self.startTime = str(self.startTime)[:-7]
        self.stopTime = str(self.stopTime)[:-7]
        self.report_href = "{}/{}.html".format(self.case_name, self.case_name)
        if not outcome.success:
            for i in outcome.errors:
                if i[1]:
                    t = i[1]
                    self.message = "{}：{}".format(str(t[0])[8:-2], t[1])
                    break

    def parse_doc(self, doc):
        """从当前用例doc解析出用例信息,如Title"""
        if doc:
            ret = re.search(r'@Title:(.*)', doc)
            if ret:
                self.case_title = ret.group(1)

    def add_sn(self):
        """为每条case的测试报告添加sn设备名称"""
        self.device_sn = self.name
