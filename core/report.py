# !/usr/bin/env python
# coding: utf-8
# @project_name: autoTest-new
# @user: QM1997
# @time: 2019/4/26 0:14
# @desc:

import os
import re
import copy
import datetime
from core.var import VAR
from settings import BASE_DIR
from jinja2 import Template


def generate_case_report(self, name, report_dir_list):
    """self:instance of TestCase"""
    if VAR.mode != 1:
        return
    for casehtml in report_dir_list:
        if name in casehtml:
            p = os.path.join(BASE_DIR, "reportResource", "template0.html")
            with open(p, encoding='utf-8') as f:
                content = f.read()
            template = Template(content)
            setup_msg, test_msg, teardown_msg = get_self_log(self)
            context = {
                "case": self,
                "setup_msg": setup_msg,
                "test_msg": test_msg,
                "teardown_msg": teardown_msg,
            }
            t = template.render(context)
            case_path = os.path.join(casehtml, self.case_name)
            self.report_path = os.path.join(case_path, "{}.html".format(self.case_name))
            with open(self.report_path, "w", encoding='utf-8') as f:
                f.write(t)
                f.flush()
            log_path = os.path.join(casehtml, name + "_all_log.log")
            f = open(log_path, "a+", encoding='utf-8')
            for k, v in context.items():
                if k == 'setup_msg':
                    for i in v:
                        if i[0] == 'info' or i[0] == 'error':
                            f.writelines(i[1] + ' ')
                            f.writelines(i[2]+'\n')
                elif k == 'test_msg':
                    for i in v:
                        if i[0] == 'info' or i[0] == 'error':
                            f.writelines(i[1] + ' ')
                            f.writelines(i[2] + '\n')
                elif k == 'teardown_msg':
                    for i in v:
                        if i[0] == 'info' or i[0] == 'error':
                            f.writelines(i[1] + ' ')
                            f.writelines(i[2] + '\n')
                    f.writelines("\n")
            f.close()
            t = 'Generate TestCase Report > {}'.format(self.report_path)
            self.log.info(t)


def get_self_log(self):
    info = VAR.stdout.get_value()
    err = VAR.stderr.get_value()
    case_info = info[self.case_name] if self.case_name in info else []
    case_err = err[self.case_name] if self.case_name in err else []
    case_msg = [("info", *i) for i in case_info] + [("error", *i) for i in case_err]
    case_msg = bubble_sort(case_msg)  # 排序
    case_msg = [_x(i) for i in case_msg]  # 处理每个log的显示情况
    # case_msg = x_(case_msg)  # 将error的前一个keyword标记为error
    return __x(case_msg)  # 截断log为三段


def x_(case_msg):
    """将error的前一个keyword,标记为error"""
    copy_case_msg = copy.deepcopy(case_msg)
    for i, j in enumerate(case_msg):
        if j[0] == "error" and not j[3]:
            k = _find(copy_case_msg, i)
            if k:
                copy_case_msg[k][0] = "error"
    # 如果setup end 是error的话,setup start 也标记为error,以此类推
    copy_case_msg = x__(copy_case_msg)
    return copy_case_msg


def x__(case_msg):
    print("case_msg:", case_msg)
    """如果setup end 是error的话,setup start 也标记为error,以此类推"""
    d = {
        "setUp_start": None,
        "setUp_end": None,  #  <class 'tuple'>: (5, ['info', '2018-05-07 15:55:22.837', '--------- Test_001 setUp end  ----------', 'setUp_end'])
        "test_start": None,
        "test_end": None,
        "tearDown_start": None,
        "tearDown_end": None,
    }
    for i, j in enumerate(case_msg):
        if j[3] in list(d.keys()):
            d[j[3]] = (i, j)
    if d['setUp_end'] and d['setUp_end'][1][0] == "error":
        case_msg[d["setUp_start"][0]][0] = "error"
    if d['test_end'] and d['test_end'][1][0] == "error":
        case_msg[d["test_start"][0]][0] = "error"
    if d['tearDown_end'] and d['tearDown_end'][1][0] == "error":
        case_msg[d["tearDown_start"][0]][0] = "error"
    return case_msg


def _find(case_msg,index):
    copy_case_msg = copy.deepcopy(case_msg)
    for i in case_msg[index-1::-1]:
        if i[3] and i[3] not in ["img_path",]:
            return copy_case_msg.index(i)


def __x(case_msg):
    """截断log为三段"""
    copy_case_msg = copy.deepcopy(case_msg)
    setup_end_k = None
    test_end_k = None
    for i in case_msg:
        # if i[3]:
        #     if "setUp_end" == i[3]:
        #         setup_end_k = copy_case_msg.index(i)
        #     elif "test_end" == i[3]:
        #         test_end_k = copy_case_msg.index(i)
        if i[2]:
            if "setUp end" in ''.join(i):
                setup_end_k = copy_case_msg.index(i)
            elif "test end" in ''.join(i):
                test_end_k = copy_case_msg.index(i)
    if not test_end_k:
        # 说明只执行了Setup,且发生了错误,test和teardown都没有执行
        return copy_case_msg, [], []
    return copy_case_msg[0:setup_end_k + 1], copy_case_msg[setup_end_k + 1:test_end_k + 1], copy_case_msg[test_end_k + 1:]


def _x(i):
    """处理每个log的显示情况"""
    i = list(i)
    if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}', i[2]):
        a, b = i[2][23:].split(":", maxsplit=1)
        i[2] = b.strip()
    i[2] = i[2].strip("\n")
    if len(i) == 3:
        i.append("")
    if i[3] == "img_path":
        t = os.path.join(os.path.split(os.path.dirname(i[2]))[1], os.path.basename(i[2]))
        i[2] = t
    return i


def gt(t1, t2):
    # t1 t2 类似2018-06-27 10:16:13:658 这样的字符串
    t1 = t1[1]
    t2 = t2[1]
    _t1, __t1 = t1.split(".")
    _t2, __t2 = t2.split(".")
    _t1 = datetime.datetime.strptime(_t1, "%Y-%m-%d %H:%M:%S")
    _t2 = datetime.datetime.strptime(_t2, "%Y-%m-%d %H:%M:%S")
    if _t1 == _t2:
        if int(__t1) == int(__t2):
            return False
        elif int(__t1) > int(__t2):
            return True
        elif int(__t1) < int(__t2):
            return False
    elif _t1 > _t2:
        return True
    elif _t1 < _t2:
        return False


def bubble_sort(li):
    for i in range(len(li) - 1):
        for j in range(len(li) - i - 1):
            if gt(li[j], li[j + 1]):
                li[j], li[j + 1] = li[j + 1], li[j]
    return li


def generate_task_report(name, res):
    """self:instance of result"""
    if VAR.mode != 1:
        return
    # res.msg_again = 1
    # if len(res.errors) > 0 or len(res.failures) > 0:
    #     res.task_status = "fail"
    #     # res.fail_cases_count = len(res.errors) + len(res.failures)
    #     res.fail_cases_count = VAR.failed
    #     res.pass_cases_count = res.testsRun - res.fail_cases_count
    if VAR.failed > 0:
        res.task_status = "fail"
        res.fail_cases_count = VAR.failed
        res.pass_cases_count = res.testsRun - VAR.failed
        if res.pass_cases_count == 0:
            res.passing_rate = 0
        else:
            res.passing_rate = float('%.2f' % (res.pass_cases_count/res.testsRun))*10*10
    elif VAR.failed == 0:
        res.task_status = "success"
        res.pass_cases_count = res.testsRun  # result.testsRun: 3  测试套中case的个数
        res.fail_cases_count = 0
        res.passing_rate = 100

    p = os.path.join(BASE_DIR, "reportResource", "template1.html")
    with open(p, encoding='utf-8') as f:
        content = f.read()
    template = Template(content)
    for i in VAR.report_dir_list:
        if name in i:
            context = {"result": res}
            t = template.render(context)
            res.report_path = os.path.join(i, "taskReport.html")
            f = open(res.report_path, "w", encoding='utf-8')
            f.write(t)
            f.flush()
            t = 'Generate Task Report > {}'.format(res.report_path)
            res.log.info(t)
            msg = "ALL Task Done，{} about The Test Result is Total：{}  Pass：{}  Failed：{}".format(name, res.testsRun, res.testsRun - VAR.failed, VAR.failed)
            res.log.info(msg)
