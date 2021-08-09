# -*- encoding: utf-8 -*-
"""
@File    : var.py
@Project : autoText-rebuild
@Time    : 2019/12/17 17:47
@Author  : qm
@Email   : quming5@xiaomi.com
@desc    :
"""
import datetime
import sys
import os
import settings


class ConfigNotExistError(Exception):
    pass


class ConfigParseError(Exception):
    pass


def _mode():
    mode = 1  # 模式1是正常执行,模式2是执行选择的文件,模式3是执行选择的区域
    if len(sys.argv) > 1:
        _, _, file_path, start_line, end_line, *args = sys.argv
        print("args:", str(args))
        if not args:  # 当执行模式是2(用例文件执行alt+Q),args列表为空集合
            mode = 2
        else:
            mode = 3
    return mode


class Variable(dict):

    def __init__(self, *args, **kwargs):
        super(Variable, self).__init__(*args, **kwargs)
        if "config" in kwargs:
            self.config = kwargs["config"]
        else:
            # self.config = _config()
            self.config = settings.Var

    def __getattr__(self, name):
        if not name in self.config:
            if name in ["cur_case_name", ]:
                return
            else:
                raise Exception('config has no attr "{}"'.format(name))
        value = self.config[name]
        if isinstance(value, dict):
            value = Variable(config=value)
        return value


VAR = Variable()
VAR.mode = _mode()


def get_devices():
    device_list = []
    devices = list(set(os.popen("adb devices", "r").read().split()[4:]))
    devices.remove("device")
    for device in devices:
        device_list2 = []
        name = os.popen("adb -s " + device + " shell getprop ro.product.model").read().replace(' ', '')
        device_list2.append(name.strip())
        device_list2.append(device)
        device_list.append(device_list2)
    setattr(VAR, "device_dict", dict(device_list))
    return dict(device_list)

# def get_devices2():
#     device_list = []
#     devices = list(set(os.popen("adb devices", "r").read().split()[4:]))
#     devices.remove("device_MIUI11")
#     for device_MIUI11 in devices:
#         device_list2 = []
#         name = os.popen("adb -s " + device_MIUI11 + " shell getprop ro.build.version.release").read()
#         device_list2.append(name.strip())
#         device_list2.append(device_MIUI11)
#         device_list.append(device_list2)
#     setattr(VAR, "device_dict", dict(device_list))
#     return dict(device_list)


def make_reportDir():
    VAR.project_start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")  # -%S
    report_dir_list = []
    for NAME_, SN_ in get_devices().items():
        android_version = os.popen("adb -s " + SN_ + " shell getprop ro.build.version.release").read().strip()
        Name_ = NAME_ + "_" + SN_ + "_android" + android_version
        report_dir = os.path.join(settings.BASE_DIR, VAR.report_folder, "task_{}".format(VAR.project_start_time), Name_)
        report_dir_list.append(report_dir)
        if VAR.mode == 1 and not os.path.exists(report_dir):
            os.makedirs(report_dir, exist_ok=True)
    VAR.report_dir_list = report_dir_list


make_reportDir()


class TimeList(object):
    def __init__(self):
        self.d = {}

    def append(self, *args):
        if len(args) == 1 and args[0] == "\n":
            return
        if VAR.cur_case_name:
            cur_case_name = VAR.cur_case_name
        else:
            cur_case_name = "contrib"
        if cur_case_name in self.d:
            self.d[cur_case_name].append((self.now, *args))
        else:
            self.d[cur_case_name] = [(self.now, *args), ]

    @property
    def now(self):
        # ct = time.time()
        # local_time = time.localtime(ct)
        # data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        # data_secs = (ct - int(ct)) * 1000
        # time_stamp = "%s.%03d" % (data_head, data_secs)
        return str(datetime.datetime.now())[:-3]


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp
        self.l = TimeList()

    def write(self, s, **kwargs):
        self.fp.write(s)  # ,encoding='utf-8'
        self.l.append(s, *list(kwargs.keys()))

    def flush(self):
        self.fp.flush()

    def get_value(self):
        return self.l.d


def _exec():
    mode = VAR.mode
    if mode != 1:
        _, _, file_path, start_line, end_line, *args = sys.argv
        with open(file_path, encoding="utf-8") as f:
            t = f.readlines()[int(start_line) - 1:int(end_line)]
        if mode == 2:
            with open(os.path.join(settings.BASE_DIR, "scripts", "scripts"), "w", encoding="utf-8") as f:
                f.write(file_path)
        elif mode == 3:
            with open(os.path.join(settings.BASE_DIR, "scripts", "Temp.py"), "w", encoding="utf-8") as f:
                t = ["        {}".format(i.strip(" ")) for i in t]
                f.write(settings.CONTENT.replace("{{ content }}", "".join(t)))


_exec()

VAR.stdout = sys.stdout = OutputRedirector(sys.stdout)
VAR.stderr = sys.stderr = OutputRedirector(sys.stderr)
