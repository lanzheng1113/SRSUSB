# -*_coding:gb2312-*-
import os
import sqlite3
import codecs
import winsupport
import re
import hashlib
import subprocess
from optparse import OptionParser


config = {
    "Allx64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "5.1|5.2|6.0|6.1|6.2|6.3|10.0",
        "primary" : "yes"
    },
    "Allx86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "5.1|5.2|6.0|6.1|6.2|6.3|10.0",
        "primary" : "yes"
    },
    "Nt6x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.0|6.1|6.2|6.3|10.0",
        "primary" : "yes"
    },
    "Nt6x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.0|6.1|6.2|6.3|10.0",
        "primary" : "yes"
    },
    "Win7x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.1",
        "primary" : "yes"
    },
    "Win7x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.1",
        "primary" : "yes"
    },
    "Win8x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.2",
        "primary" : "yes"
    },
    "Win8x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.2",
        "primary" : "yes"
    },
    "Win10x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "10.0",
        "primary" : "yes"
    },
    "Win10x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "10.0",
        "primary" : "yes"
    },
    "Win78x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.1|6.2",
        "primary" : "yes"
    },
    "Win78x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.1|6.2",
        "primary" : "yes"
    },
    "Win81x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.3",
        "primary" : "yes"
    },
    "Win81x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.3",
        "primary" : "yes"
    },
    "Win881x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.2|6.3",
        "primary" : "yes"
    },
    "Win881x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.2|6.3",
        "primary" : "yes"
    },
    "Win8110x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.3|10.0",
        "primary" : "yes"
    },
    "Win8110x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.3|10.0",
        "primary" : "yes"
    },
    "Win88110x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.2|6.3|10.0",
        "primary" : "yes"
    },
    "Win88110x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.2|6.3|10.0",
        "primary" : "yes"
    },
    "WinXPx64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "5.1",
        "primary" : "yes"
    },
    "WinXPx86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "5.1",
        "primary" : "yes"
    },
    "WinVx64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.0|6.1|6.2|6.3|10.0",
        "primary" : "yes"
    },
    "WinVx86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.0|6.1|6.2|6.3|10.0",
        "primary" : "yes"
    }
}


class DriverItem:
    u"""
    驱动
    """
    is_valid = False
    hardware_id = ""
    device_class_guid = ""
    device_class_name = ""
    device_unknown_1 = ""
    device_describe = ""
    inf_relate_path = ""
    inf_section_name = ""
    inf_arch_tag = ""
    inf_os_version = ""
    device_unknown_3 = ""
    device_unknown_4 = ""
    device_unknown_5 = ""
    driver_release_time = ""
    driver_version = ""
    folder = ""
    default_os_ver = ""

    def __init__(self, string_device, v_default_os_ver):
        sl = string_device.split('|')
        if len(sl) <= 1:
            self.is_valid = False
            return
        if len(sl) != 17:
            print "Bad line [{0}],cnt={1}".format(string_device,len(sl))
            return
        self.hardware_id = sl[1].upper()
        self.device_class_guid = sl[2]
        self.device_class_name = sl[3]
        self.device_unknown_1 = sl[4]
        self.device_describe = sl[5]
        self.inf_relate_path = sl[6]
        self.inf_section_name = sl[7]
        self.inf_arch_tag = sl[8]
        self.inf_os_version = sl[9]
        self.device_unknown_3 = sl[10]
        self.device_unknown_4 = sl[11]
        self.device_unknown_5 = sl[12]
        self.driver_release_time = sl[13]
        self.driver_version = sl[14]
        self.folder = sl[15]
        self.default_os_ver = v_default_os_ver
        # ql2300;ql2300.sys
        # if self.device_unknown_1 != "":
        #    print u"奇异的4号:{0},在[{1}]中".format(self.device_unknown_1, string_device)
        temp_str = self.inf_arch_tag.upper()
        if temp_str != "NTAMD64" and temp_str != "NTX86" and temp_str != "NTIA64":
            # print u"奇异的arch_tag:{0},在[{1}]中".format(self.inf_arch_tag, string_device)
            if self.inf_arch_tag != "":
                self.inf_arch_tag = ""
        if self.inf_os_version != "" \
                and self.inf_os_version != "5.1" \
                and self.inf_os_version != "5.2" \
                and self.inf_os_version != "6.0" \
                and self.inf_os_version != "6.1" \
                and self.inf_os_version != "6.2" \
                and self.inf_os_version != "6.3" \
                and self.inf_os_version != "10.0":
            # print u"奇异的os_version:{0},在[{1}]中".format(self.inf_os_version, string_device)
            self.inf_os_version = ""
        # if self.device_unknown_3 != "":
        #    print u"奇异的10号:{0},在[{1}]中".format(self.device_unknown_3, string_device)
        #    return
        # if self.device_unknown_4 != "":
        #    print u"奇异的11号:{0},在[{1}]中".format(self.device_unknown_4, string_device)
        #    return
        # 6.1
        # if self.device_unknown_5 != "":
        #    print u"奇异的12号:{0},在[{1}]中".format(self.device_unknown_5, string_device)
        #    return
        self.is_valid = True
        return

    def try_combine(self, item_compare):
        if self.is_valid and item_compare.is_valid:
            # 硬件ID，架构，驱动版本，发布时间相同
            if self.hardware_id == item_compare.hardware_id \
                    and self.device_class_guid == item_compare.device_class_guid\
                    and self.device_class_name == item_compare.device_class_name\
                    and self.driver_release_time == item_compare.driver_release_time\
                    and self.driver_version == item_compare.driver_version\
                    and self.inf_relate_path == item_compare.inf_relate_path\
                    and self.folder == item_compare.folder\
                    and self.inf_arch_tag == item_compare.inf_arch_tag:
                # 把存在于list_it_os_version而不存在于list_my_os_version中的元素合并过来
                list_my_os_version = self.inf_os_version.split('|')
                list_it_os_version = item_compare.inf_os_version.split('|')
                for i in list_it_os_version:
                    if i not in list_my_os_version:
                        list_my_os_version.append(i)
                # 用list_my_os_version重新生成inf_os_version成员
                self.inf_os_version = '|'.join(list_my_os_version)
                return True
        return False


os_ver_bit_map = {
    "5.0": 0,
    "5.1": 1,
    "5.2": 2,
    "6.0": 3,
    "6.1": 4,
    "6.2": 5,
    "6.3": 6,
    "10.0": 7
}


def os_ver_str_to_int(str_val):
    arr = str_val.split("|")
    os_ver_with_int = 0
    for j in arr:
        if j not in os_ver_bit_map:
            print u"错误！不存在的系统版本！"
        else:
            bit_map = os_ver_bit_map[j]
            os_ver_with_int = os_ver_with_int | (1 << bit_map)
    os_ver_hex_str = hex(os_ver_with_int)
    if os_ver_hex_str[0:2] == "0x" or os_ver_hex_str[0:2] == "0X":
        os_ver_hex_str = os_ver_hex_str[2:]
    return os_ver_hex_str


def os_ver_is_subset(a, b):
    u"""
    数组a 是否为 数组b的一个子集
    :param arr_a:
    :param arr_b:
    :return:
    """
    arr_a = a.split("|")
    arr_b = b.split("|")
    set_a = set(arr_a)
    set_b = set(arr_b)
    return set_a.issubset(set_b)


def fill_0_to_hex_str(hex_str):
    temp = hex_str
    while len(temp) < 4:
        temp = "0" + temp
    return temp


def remove_0x_from_hex_str(hex_str):
    if hex_str[0:2] == "0x" or hex_str[0:2] == "0X":
        ret = hex_str[2:]
        return ret
    else:
        return hex_str


def driver_ver_str_to_int(str_drv_ver):
    """
    from 2.1.5.37 to 2000100050025
    :param str_drv_ver: a version string like 2.1.5.37
    :return: a hex value with string format.
    """
    arr = str_drv_ver.split(".")
    if len(arr) != 4:
        print u"错误的版本号{0}".format(str_drv_ver)
        return "0"
    else:
        i0 = int(arr[0])
        i1 = int(arr[1])
        i2 = int(arr[2])
        i3 = int(arr[3])
        # every digit should translate to a hex-format digit string, and i1 ~ i3 should be 4 byte.
        s0 = hex(i0)
        s0 = remove_0x_from_hex_str(s0)
        s1 = hex(i1)
        s1 = remove_0x_from_hex_str(s1)
        s1 = fill_0_to_hex_str(s1)
        s2 = hex(i2)
        s2 = remove_0x_from_hex_str(s2)
        s2 = fill_0_to_hex_str(s2)
        s3 = hex(i3)
        s3 = remove_0x_from_hex_str(s3)
        s3 = fill_0_to_hex_str(s3)
        # return values;
        return s0+s1+s2+s3


manually_command = [
    'DELETE FROM s_hidandpkg WHERE HIDNAME = "Nvme Controller Fix By Www.SysCeo.Com"',
    'UPDATE s_hidandpkg SET OS="c0", OS2 = "c0" WHERE OS = "20" and OS2 = "e0" and PATH="Win88110x64\\Plus\\HP\\s100i\\SmartDQ.inf"',
    r"""
    UPDATE s_hidandpkg SET OS="60", OS2 = "60" WHERE OS = "20" and OS2 = "e0" and (
    PATH="Win88110x86\Common\Adaptec\ADP80XX\ADP80XX.inf" 
    or PATH="Win88110x64\Common\Adaptec\ADP80XX\ADP80XX.inf")""",
    r"""
    UPDATE s_hidandpkg SET OS="e0", OS2 = "e0" WHERE OS = "20" and OS2 = "e0" and (
    PATH="Win88110x86\Common\Adaptec\arcsas\arcsas.inf" 
    or PATH="Win88110x64\Common\Adaptec\arcsas\arcsas.inf" 
    or PATH = "Win88110x86\Plus\Intel\300\iaStorAC.inf"
    or PATH = "Win88110x64\Plus\Intel\300\iaStorAC.inf"
    or PATH = "Win88110x86\Plus\Intel\300\iaAHCIC.inf"
    or PATH = "Win88110x64\Plus\Intel\300\iaAHCIC.inf"
    or PATH = "Win88110x64\Plus\HP\B140i\HPSA3.inf") 
    """,
    r"""
    UPDATE s_hidandpkg SET OS="e0", OS2 = "e0" WHERE OS != OS2 AND OS2 = "e0" and (
    PATH="Win88110x64\Plus\HP\P408i_P816i\SmartPqi.inf" 
    or PATH = "Win88110x64\Plus\Intel\300\iaStorSW.inf")
    """,
    r"""UPDATE s_hidandpkg SET OS="f0", OS2 = "f0" WHERE OS != OS2 AND OS2 = "e0" and (
    PATH="Win88110x64\Plus\Intel\1020\iaAHCIC.inf" 
    or PATH = "Win88110x64\Plus\Intel\1020\iaStorAC.inf"
    or PATH = "Win88110x86\Plus\Intel\1020\iaAHCIC.inf"
    or PATH = "Win88110x86\Plus\Intel\1020\iaStorAC.inf")
    """,
    r'UPDATE s_hidandpkg SET OS="24", OS2 = "24" WHERE OS != OS2 AND OS2 = "2" and PATH="WinXPx86\Plus\Intel\3.6.0.1090\SCU\iaStorS.inf"',
    r"""UPDATE s_hidandpkg SET OS="4", OS2 = "4" WHERE OS != OS2 AND OS2 = "2" and (
    PATH="WinXPx86\Plus\Intel\C600RAID\IASTORS.INF" 
    or PATH = "WinXPx86\Plus\Intel\C600AHCI\IASTORA.INF"
    or PATH = "WinXPx64\Plus\Virtio\viostor.inf"
    or PATH = "WinXPx86\Plus\Virtio\VIOSTOR.INF")""",
    r"""
    UPDATE s_hidandpkg SET OS="8", OS2 = "8" WHERE OS != OS2 AND OS2 = "10" and (PATH="Win7x64\Common\AMD\2\ahcix64s.inf"
    or PATH = "Win7x86\Common\AMD\2\ahcix86s.inf"
    or PATH = "Win7x86\Plus\Promise\1\PegasusJ2.inf")
    """,
    r'UPDATE s_hidandpkg SET OS2 = OS WHERE OS != OS2 and OS2 = "20"',
    r'UPDATE s_hidandpkg SET OS2 = "10" WHERE OS = "10" AND OS2 = "30"',
    r'UPDATE s_hidandpkg SET OS2 = OS WHERE OS != OS2 AND OS2 = "40"',
    r"""
    UPDATE s_hidandpkg SET OS = "60" WHERE OS = "20" AND OS2 = "60" and 
    PATH = "Win881x64\Plus\QLogic\FC\x64_New\q23wx64W12Storv9.2.9.23_WHQL\ql2x00.inf"
    """,
    r"""
    UPDATE s_hidandpkg SET OS = "38",OS2 = "38" WHERE OS != OS2 and OS2 = "80" and 
    PATH = "Win10x64\Plus\Brocade\bfad\bfad.inf"
    """,
    r"""
    UPDATE s_hidandpkg SET OS = "e0",OS2 = "e0" WHERE OS != OS2 and OS2 = "80" and (
    PATH = "Win10x64\Plus\QLogic\FC\x64_New\ql2x00.inf" 
    or PATH = "Win10x64\Plus\QLogic\FC\x64\ql2x00.inf")
    """,
    r"""
    UPDATE s_hidandpkg SET OS="20",OS2 = "20" WHERE OS != OS2 and OS2 = "80" and 
    PATH = "Win10x64\Plus\QLogic\ql40xx2i_10BOOT\ql40xx2i.inf"
    """,
    r"""
    UPDATE s_hidandpkg SET OS="8",OS2 = "8" WHERE OS != OS2 and OS2 = "f8" and
    (PATH = "Nt6x86\Plus\HP\hpcissx2\hpcissx2.inf" 
    or PATH = "Nt6x86\Plus\HP\B120i_B320i\hpsa2.inf" 
    or PATH = "Nt6x86\Plus\ToshibaM400\KR10.INF"
    or PATH = "Nt6x86\Plus\ToshibaM400\VIRTUAL.INF")
    """,
    r"""
    UPDATE s_hidandpkg SET OS2 = OS WHERE OS != OS2 and OS2 = "f8" and 
    (PATH = "Nt6x86\Plus\QLogic\ql2x00\ql2x00.inf" 
    or PATH = "WinVx64\Plus\QLogic\FC\x64\ql2x00.inf" 
    or PATH = "Nt6x64\Plus\QLogic\ql2x00\ql2x00.inf")
    """,
    r"""
    UPDATE s_hidandpkg SET OS="30",OS2 = "30" WHERE OS != OS2 and OS2 = "f8" and 
    (PATH = "Nt6x86\Common\Intel\2\iaAHCIC.inf" 
    or PATH = "Nt6x86\Common\Intel\2\iaStorAC.inf")
    """,
    r"""
    UPDATE s_hidandpkg SET OS="18",OS2 = "18" WHERE OS != OS2 and OS2 = "f8" and 
    (PATH = "Nt6x64\Plus\HP\B120i_B320i\hpsa2.inf" 
    or PATH = "WinVx64\Plus\QLogic\FCoE\x64\qlfcoe.inf" 
    or PATH = "Nt6x64\Plus\HP\hpcissx2\hpcissx2.inf")
    """,
    r"""
    UPDATE s_hidandpkg SET OS="F0",OS2 = "F0" WHERE OS != OS2 and OS2 = "f8" and 
    (PATH = "Nt6x86\Common\Intel\Nvme\IaNVMe.inf" 
    or PATH = "Nt6x64\Common\Intel\Nvme\IaNVMe.inf" 
    or PATH = "Nt6x64\Common\Intel\2\iaAHCIC.inf" 
    or PATH = "Nt6x64\Common\Intel\2\iaStorAC.inf")
    """,
    r'UPDATE s_hidandpkg SET OS="38",OS2 = "38" WHERE OS != OS2 and OS2 = "f8" and PATH = "Nt6x86\Plus\Brocade\bfad\bfad.inf"',
    r"""
    UPDATE s_hidandpkg SET OS="18",OS2 = "18" WHERE OS != OS2 and OS2 = "fe" and ( 
    PATH = "Allx64\Plus\QLogic\qle_winx64v911120\ql2x00.inf" 
    or PATH = "Allx86\Plus\QLogic\qle_winv911120\ql2x00.inf" 
    or PATH = "Allx64\Plus\QLogic\qle_winx64v911018\qlfcoe.inf")
    """,
    r'UPDATE s_hidandpkg SET OS="8",OS2 = "8" WHERE OS != OS2 and OS2 = "fe" and PATH = "Allx86\Plus\QLogic\qle_winv911018\qlfcoe.inf"'
]


def file_name_replace(i):
    o = ""
    for c in i:
        if c == '\\' or c == '/' or c == '\'' or c == '\"' or c == '|' or c == '?' or c == '*' or c == '<' or c == '>' or c == ' ':
            o += "_"
        else:
            o += c
    return o


# 具有相同的HID PF OS DRVVER TYPE， 然而却又有不同的inf路径
recore_item_same_rec = set()
inf_path_and_7z_file_name = {}


class RecordItem:
    u"""
    新表的元素
    """
    def __init__(self, archive_folder, work_dir):
        self.hardware_id = ""
        self.device_describe = ""
        self.inf_relate_path = ""
        self.inf_os_version = ""
        self.inf_arch_tag = ""
        self.device_class_name = ""
        self.driver_version = ""
        self.driver_release_time = ""
        self.name_7z_file = ""
        self.password = ""
        self.archive_folder = archive_folder
        self.work_dir = work_dir

    def make_7z_with_pswd(self):
        """
        return
        :return:
        """
        if self.inf_arch_tag == '0':
            arch_str = "x86"
        elif self.inf_arch_tag == '9':
            arch_str = "x64"
        else:
            arch_str = "archx"
        repeat_index = 0
        is_repeat = True
        while is_repeat:
            name = "{0}_{1}_{2}_{3}_{4}_n{5}.7z".format(self.device_class_name, self.device_describe,
                                                        self.inf_os_version, arch_str,
                                                        self.driver_version, repeat_index)
            name = file_name_replace(name)
            full_path = os.path.join(self.archive_folder, name)
            if os.path.exists(full_path):
                repeat_index += 1
            else:
                break
        self.name_7z_file = name
        md5_obj = hashlib.md5()
        md5_obj.update(self.name_7z_file)
        temp = md5_obj.hexdigest()
        md5_obj_2 = hashlib.md5()
        md5_obj_2.update(temp)
        temp = md5_obj_2.hexdigest()
        self.password = temp[:8]
        inf_full_path = self.work_dir + "\\" + self.inf_relate_path
        if os.path.exists(inf_full_path) and os.path.isfile(inf_full_path):
            process_cmd = '"E:\\Program Files\\7-Zip\\7z.exe" a "{0}" -p{1} -mhe -y "{2}\\*"'.format(full_path, self.password, os.path.dirname(inf_full_path))
            if 0 != subprocess.call(process_cmd):
                raise Exception(u"执行命令{0}时出现了异常。".format(process_cmd))
        else:
            raise Exception(u"路径{0}不存在或者不是一个文件".format(inf_full_path))

    def try_combine_version(self, another_element):
        if self.hardware_id == another_element.hardware_id and \
                self.inf_arch_tag == another_element.inf_arch_tag and \
                self.driver_version == another_element.driver_version and \
                self.device_class_name == another_element.device_class_name:
            if self.inf_os_version == another_element.inf_os_version:
                if self.inf_relate_path != another_element.inf_relate_path:
                    cond = u'(HID = "{0}" AND PF = "{1}" AND OS = "{2}" AND DRVVER = "{3}" AND TYPE = "{4}")'.format(self.hardware_id, self.inf_arch_tag, self.inf_os_version, self.driver_version, self.device_class_name)
                    if cond not in recore_item_same_rec:
                        recore_item_same_rec.add(cond)
                    return None
                else:
                    return another_element
            else:
                # 需要合并的是inf_os_version
                osv_this = int(self.inf_os_version, 16)
                osv_another = int(another_element.inf_arch_tag, 16)
                # 只需要简单做位或操作就可以了。
                osv_combine = osv_this | osv_another
                os_ver_hex_str = hex(osv_combine)
                if os_ver_hex_str[0:2] == "0x" or os_ver_hex_str[0:2] == "0X":
                    os_ver_hex_str = os_ver_hex_str[2:]
                another_element.inf_os_version = os_ver_hex_str
                return another_element
        else:
            return None


class SrsTransport:
    __objs_driver_item_primary = {}  # 这个对象将存放到主表
    __objs_driver_item_2nd = {}  # 这个对象将存放到副表
    __work_dir = ""
    __archive_folder = ""
    __combine_count = 0
    __ignore_count = 0
    __sqlite_file = "drivers.dat"
    __sqlite_file_full_path = ""
    __item_count_in_files = 0
    __insert_count = 0

    def __init__(self, v_work_dir, archive_folder):
        self.__work_dir = v_work_dir
        self.__archive_folder = archive_folder
        self.offical_repeat_records = 0

    def dump(self):
        print "count of 1st element: {0}".format(len(self.__objs_driver_item_primary.keys()))
        print "count of 2nd element: {0}".format(len(self.__objs_driver_item_2nd.keys()))
        print "total combined count: {0}".format(self.__combine_count)
        print "total count ignore: {0}".format(self.__ignore_count)
        print "total insert count: {0}".format(self.__insert_count)
        print "total item count in files : {0}".format(self.__item_count_in_files)

    def commit_raw_records(self):
        self.__sqlite_file_full_path = os.path.join(self.__work_dir, self.__sqlite_file)
        if os.path.exists(self.__sqlite_file_full_path):
            conn = sqlite3.connect(self.__sqlite_file_full_path)
            c = conn.cursor()
            table_name = "s_hidandpkg"
            for k, v in self.__objs_driver_item_primary.items():
                obj_array = v
                for i in obj_array:
                    if i.folder == "Win8x64" and i.inf_relate_path == r"Common\LSI\SAS3\LSI_SAS3.inf" and i.inf_arch_tag == "x86":
                        print u"break here."
                    relate_path_of_inf = i.folder + "\\" + i.inf_relate_path
                    arch_number_type = "0"
                    if i.inf_arch_tag.lower() == "x64":
                        arch_number_type = "9"
                    elif i.inf_arch_tag.lower() == "x86":
                        arch_number_type = "0"
                    else:
                        continue
                    if os_ver_is_subset(i.default_os_ver, i.inf_os_version):
                        def_os_ver_str = os_ver_hex_str = os_ver_str_to_int(i.inf_os_version)
                    else:
                        os_ver_hex_str = os_ver_str_to_int(i.inf_os_version)
                        def_os_ver_str = os_ver_str_to_int(i.default_os_ver)
                    hex_driver_ver = driver_ver_str_to_int(i.driver_version)
                    insert_str = "INSERT INTO {0} " \
                                 "(HID,HIDNAME,PATH,OS,PF,TYPE,DRVVER,DRVDATE,OS2) " \
                                 "VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')" \
                        .format(table_name, i.hardware_id, i.device_describe, relate_path_of_inf,
                                os_ver_hex_str,arch_number_type, i.device_class_name, hex_driver_ver,
                                i.driver_release_time, def_os_ver_str)
                    try:
                        c.execute(insert_str)
                        self.__insert_count = self.__insert_count + 1
                    except sqlite3.OperationalError as e:
                        print u"执行{0}时发生错误{1}".format(insert_str, e)
            conn.commit()
            print u"插入完成,开始执行命令处理那些OS的值与所在目录的属性不一致的记录。"
            for update_cmd in manually_command:
                print update_cmd
                c.execute(update_cmd)
            conn.commit()
            conn.close()

    def commit_official_records(self):
        u"""
        先做去重处理，然后加密并生成7z包，并在原有的raw表上去掉OS2，增加新的列pswd保存到新表。
        :return:
        """
        conn = sqlite3.connect(self.__sqlite_file_full_path)
        c = conn.cursor()
        try:
            c.execute("SELECT HID,HIDNAME,PATH,OS,PF,TYPE,DRVVER,DRVDATE from s_hidandpkg")
        except sqlite3.OperationalError as e:
            print u"执行SELECT s_hidandpkg时发生错误{0}".format(e)
        res = c.fetchall()
        if len(res) == 0:
            conn.close()
            return 0
        else:
            print u"Get {0} records, we are now going to combine the repeat record... please wait ..."
        record_sign_and_items = {}  # key : sign-str, value RecordItem type object
        for i in res:
            it = RecordItem(self.__archive_folder, self.__work_dir)
            it.hardware_id = i[0]
            it.device_describe = i[1]
            it.inf_relate_path = i[2]
            it.inf_os_version = i[3]
            it.inf_arch_tag = i[4]
            it.device_class_name = i[5]
            it.driver_version = i[6]
            it.driver_release_time = i[7]
            has_combined = False
            sign_str = it.hardware_id + "_" +  it.inf_arch_tag + "_"+ it.driver_version + "_" + it.device_class_name
            if sign_str in record_sign_and_items:
                combined_item = it.try_combine_version(record_sign_and_items[sign_str])
                if combined_item is not None:
                    record_sign_and_items[sign_str] = combined_item
                    self.offical_repeat_records += 1
                    print u"combined item:[{0}], total:{1}".format(sign_str, self.offical_repeat_records)
                    has_combined = True
            if not has_combined:
                inf_full_path = it.work_dir + "\\" + it.inf_relate_path
                if inf_full_path in inf_path_and_7z_file_name:
                    it.password = inf_path_and_7z_file_name[inf_full_path]["password"]
                    it.name_7z_file = inf_path_and_7z_file_name[inf_full_path]["name_7z"]
                else:
                    it.make_7z_with_pswd()
                    temp_obj = {"password": it.password, "name_7z": it.name_7z_file}
                    inf_path_and_7z_file_name[inf_full_path] = temp_obj
                if it.password == "":
                     raise Exception("Fatal logic error,please check the function RecordItem::make_pswd")
                if it.name_7z_file == "":
                    raise Exception("Fatal logic error,please check the function and RecordItem::make_7z_with_pswd.")
                record_sign_and_items[sign_str] = it
        table_name = "s_hidandpkg_ofc"
        for j, i in record_sign_and_items.items():
            insert_str = "INSERT INTO {0} " \
                         "(HID,HIDNAME,PATHINF,PATH,OS,PSWD7z,PF,TYPE,DRVVER,DRVDATE) " \
                         "VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')" \
                .format(table_name, i.hardware_id, i.device_describe, i.inf_relate_path,
                        i.name_7z_file, i.inf_os_version, i.password, i.inf_arch_tag, i.device_class_name,
                        i.driver_version, i.driver_release_time)
            try:
                c.execute(insert_str)
            except sqlite3.OperationalError as e:
                print u"执行{0}时发生错误{1}".format(insert_str, e)
        conn.commit()
        conn.close()
        return

    def tran(self, sc_index, default_arch, default_os_ver, is_primary):
        sc_index_full_path = os.path.join(self.__work_dir, sc_index)
        if not os.path.exists(sc_index_full_path):
            print u"错误！sc_index文件[{0}]不存在".format(sc_index_full_path)
            return False
        # 读文件，获取DriverItem对象列表
        file_object = open(sc_index_full_path, 'r')
        inf_object_array = []
        for line in file_object:
            line = line.strip('\r')
            line = line.strip('\n')
            dr = DriverItem(line, default_os_ver)
            if dr.is_valid:
                inf_object_array.append(dr)
                self.__item_count_in_files = self.__item_count_in_files + 1
        file_object.close()
        # 检查，如必要则用默认的arch, os_ver替换DriverItem中对应的值
        for i in inf_object_array:
            relate_path_of_inf = i.folder + "\\" + i.inf_relate_path
            temp_str = i.inf_arch_tag.upper()
            arch = ""
            if "NTAMD64" == temp_str:
                arch = "x64"
            elif "NTX86" == temp_str:
                arch = "x86"
            elif "NTIA64" == temp_str:
                continue
            else:
                arch = default_arch
            # 注意这里：DriverItem对象的inf_arch_tag成员已经统一从NTAMD64/NTX86/NTIA64更换为x64/x86/ia64
            i.inf_arch_tag = arch
            #
            # 默认的arch和文件夹中带的arch名字相反，一定是在写配置的时候发生错误了
            #
            if temp_str == "":
                if (i.inf_arch_tag == "x86" and -1 != i.folder.find("x64")) or \
                        (i.inf_arch_tag == "x64" and -1 != i.folder.find("x86")):
                    # print u"跳过错误的项[{0}]-[{1}]-[{2}],文件{3}"\
                    #    .format(i.hardware_id, relate_path_of_inf, i.inf_arch_tag, sc_index_full_path)
                    self.__ignore_count = self.__ignore_count + 1
                    continue
            else:
                # 自带arch, 但是arch的名字和配置的名字相反。我们需要输出警告
                inf_full_path = os.path.join(self.__work_dir, relate_path_of_inf)
                if i.inf_arch_tag == "x86" and -1 != i.folder.find("x64"):
                    # print u"---"
                    # print u"检查可疑项[{0}],在文件{1}".format(relate_path_of_inf, sc_index_full_path)
                    if (not self.__inf_check(inf_full_path, "x86")) \
                            or (not self.__check_sys_arch(inf_full_path, False)):
                        print u"跳过架构设置(arch)可能有问题的项{0}[{1}]-[{2}]-[{3}] (inf_arch = x86)"\
                            .format(inf_full_path,i.hardware_id, i.inf_arch_tag, sc_index_full_path)
                        self.__ignore_count = self.__ignore_count + 1
                        continue
                    #else:
                        # print u"通过检测。"
                if i.inf_arch_tag == "x64" and -1 != i.folder.find("x86"):
                    # print u"---"
                    # print u"检查可疑项[{0}]-[{1}]-[{2}],在文件{3}".format(i.hardware_id, relate_path_of_inf, i.inf_arch_tag, sc_index_full_path)
                    if (not self.__inf_check(inf_full_path, "x64")) \
                            or (not self.__check_sys_arch(inf_full_path, True)):
                        print u"跳过架构设置(arch)可能有问题的项{0}[{1}]-[{2}]-[{3}] (inf_arch = x64)"\
                            .format(inf_full_path, i.hardware_id, i.inf_arch_tag, sc_index_full_path)
                        self.__ignore_count = self.__ignore_count + 1
                        continue
                    # else:
                        # print u"通过检测。"
            # 这里是更换系统版本，文本中有空，我们写入数据库的时候不能为空。这个值可以是多个系统版本号的联合
            # 如 : 5.1|5.2|6.0|6.1|6.2|6.3|10.0
            if i.inf_os_version == "":
                i.inf_os_version = default_os_ver

            if relate_path_of_inf == r"Win8x64\Common\LSI\SAS3\LSI_SAS3.inf" and arch == "x86":
                print u"break here."
            #
            # 接下来我们把这个对象归类存放到__objs_driver_item中，以如下的形式
            # sample_data1 = "SCSI\ENCLOSURELSILOGICSASX28_A.0______": [sct_object1, sect_object2, sect_object3]
            # arr = [sample_data1, sample_data2, sample_data3]
            #
            if is_primary:
                to_insert_obj_map = self.__objs_driver_item_primary
            else:
                to_insert_obj_map = self.__objs_driver_item_2nd
            if i.hardware_id not in to_insert_obj_map.keys():
                new_obj_array = [i]
                to_insert_obj_map[i.hardware_id] = new_obj_array
                if i.folder == "Win8x64" and i.inf_relate_path == r"Common\LSI\SAS3\LSI_SAS3.inf" and arch == "x86":
                    print u"break here."
            else:
                obj_array = to_insert_obj_map[i.hardware_id]
                # 如果存在，则一定不能为空。首次添加数组时一定会同时加入一个元素。
                if len(obj_array) == 0:
                    raise Exception('Empty object array!')
                else:
                    for obj in obj_array:
                        if i.try_combine(obj):
                            # 如果try_combine成功执行，那么obj已经合并到i需要删除掉obj
                            self.__combine_count = self.__combine_count + 1
                            del obj_array[obj_array.index(obj)]
                            break
                    obj_array.append(i)
                # 不需要用to_insert_obj_map[i.hardware_id] = obj_array将修改后的obj_array保存回去
                # 因为在python中obj_array = to_insert_obj_map[i.hardware_id]是将to_insert_obj_map[i.hardware_id]的引用
                # 给了变量obj_array，当obj_array发生改变时to_insert_obj_map[i.hardware_id]同时发生改变。
        return True

    def __check_sys_arch(self, inf_file_full_path, is_x64_or_x86):
        u"""
        读inf获取sys文件并判断其架构(amd64/x86)，如果读取到的任意一个sys不是指定架构则返回False，否则返回True。
        如果inf里没有任何关于sys文件的描述，那么从inf的同级目录下寻找sys文件，如果读取到的第一个sys不是指定架构则
        返回False，否则返回True。
        如果以上步骤均未找到sys文件那么将返回True.
        :param inf_file_full_path:
        :param is_x64_or_x86: True = amd64, False = x86
        :return:
        """
        directory_name = os.path.dirname(inf_file_full_path)
        file_encoding = ""
        file_object = open(inf_file_full_path, 'r')
        str_bom = file_object.read(2)
        if str_bom == '\xFF\xFE':
            file_encoding = "utf-16-le"
        if file_encoding != "":
            file_object.close()
            file_object = codecs.open(inf_file_full_path, 'r', file_encoding)
        processed_sys_file = []
        return_value = True
        has_checked = False
        for line in file_object:
            l = line.strip('\r')
            l = l.strip('\n')
            pos = l.find(".sys")
            if pos != -1:
                r = re.search("(\\w+).sys", l)
                if r is not None:
                    span = r.span()
                    if span is not None and len(span) >= 2:
                        fn = l[span[0]: span[1]]
                        if fn not in processed_sys_file:
                            processed_sys_file.append(fn)
                            full_sys_path = os.path.join(directory_name, fn)
                            if os.path.exists(full_sys_path):
                                if is_x64_or_x86:
                                    bx = (winsupport.is_pe_64(full_sys_path) == 1)
                                    # print u"check file {0} x64：{1}".format(full_sys_path,bx)
                                else:
                                    bx = (winsupport.is_pe_64(full_sys_path) == 0)
                                    # print u"检查文件{0}是否为x86：{1}".format(full_sys_path,bx)
                                if not bx:
                                    return_value = False
                                    has_checked = True
                                break
        file_object.close()
        if not has_checked:
            directory_name = os.path.dirname(inf_file_full_path)
            for root, dirs, files in os.walk(directory_name):
                for f in files:
                    ext_name = f[-4:]
                    ext_name = ext_name.lower()
                    if ext_name == ".sys":
                        full_sys_path = os.path.join(root, f)
                        if is_x64_or_x86:
                            bx = (winsupport.is_pe_64(full_sys_path) == 1)  # `winsupport` 是自定义扩展
                            # print u"check file {0} x64：{1}".format(full_sys_path, bx)
                        else:
                            bx = (winsupport.is_pe_64(full_sys_path) == 0)  # `winsupport` 是自定义扩展
                            # print u"检查文件{0}是否为x86：{1}".format(full_sys_path, bx)
                        if not bx:
                            return_value = False
                            has_checked = True
                        break
        if not has_checked:
            print u"存在一个文件{0}无法确认是X64还是X86！！！".format(inf_file_full_path)
        return return_value

    def __inf_check(self, inf_file_path, arch_to_check):
        u"""
        检查INF文件是否支持参数指定的架构，函数通过在文件中搜索[manufacturer]的值判断。
        :param inf_file_path: 需要检查的INF文件
        :param arch_to_check: 需要检查的架构类型，x86/x64之一，不支持ia64
        :return: 如果在INF文件的[manufacturer]一节中找到了需要检查的架构（x64/x86）标记(NTAMD64/NTX86)则返回TRUE，否则返回FALSE。
        """
        if arch_to_check != "x64" and arch_to_check != "x86":
            return False
        to_find1 = "NTAMD64"
        if arch_to_check == "x86":
            to_find1 = "NTX86"
        file_object = open(inf_file_path,'r')
        encoding = ""
        str_bom = file_object.read(2)
        if str_bom == '\xFF\xFE':
            encoding = 'utf-16-le'
        if encoding != "":
            file_object.close()
            file_object = codecs.open(inf_file_path, 'r', encoding)
        mark_next_line = False
        for line in file_object:
            line = line.strip('\r')
            line = line.strip('\n')
            if mark_next_line:
                # 寻找标记直到下一节[xxx]
                if line.find("[") != -1:
                    break
                # find in this line
                up = line.upper()
                if up.find(to_find1) != -1:
                    file_object.close()
                    return True
            else:
                lo = line.lower()
                if lo.find("[manufacturer]") != -1:
                    mark_next_line = True
        file_object.close()
        if not mark_next_line:
            print u"Not find manufacturer"
        return False


def load_driver_items_from_file_to_sqlite3_db_and_combine_records(v_work_dir, archive_folder):
    """
    (1) Load the Hardware id (HID) and its correspond driver from `.ScIndex` file of `CEOMSX` , check and insert record
    to the database if it is valid.
    (2) Combine the `OS version` between two records which have the same 'HID',"PF(architecture)","DRVVER(driver
    version) etc."
    (3) Call the SQL in `manually_command` array to fix the records which `OS` is not same as 'OS2 (Default OS limit by
    the folder name such as `Win8110x64`)', the `manually_command` SQL is made manually as the array name shows.
    (4) Save the records from 's_hidandpkg' to `s_hidandpkg_ofc`, the `s_hidandpkg_ofc` remove the 'OS2' and add
    'PATHINF'/'PSWD7z' column.
     """
    sct = SrsTransport(v_work_dir, archive_folder)
    for k, j in config.items():
        fn = k
        default_arch = j["d_arch"]
        default_os_ver = j["d_os_ver"]
        if j["primary"] == "yes":
            is_primary = True
        else:
            is_primary = False
            print u"插入表2"
        if not sct.tran(fn, default_arch, default_os_ver, is_primary):
            print u"转换失败"
        else:
            print u"转换成功"
    print u"完成"
    sct.commit_raw_records()
    sct.commit_official_records()
    sct.dump()
    print u"具有相同的HID PF OS DRVVER TYPE， 然而却又有不同的inf路径: {0}".format(len(recore_item_same_rec))
    for i in recore_item_same_rec:
        print i
    return


class SQLite3Compire:
    """ This class is designed to compare the records which have the same `HID` and `PF` pair in the sqlite database
     table `s_hidandpkg` and `s_hidandpkg_fi`. Note: `s_hidandpkg` is generated from the `.ScIndex` configure file of
     'CEOMSX', and `s_hidandpkg_fi` is generated from the `.inf` file of `CEOMSX` (Using tool `coll\Release\DPInst.exe`).
    """
    def __init__(self, sqlite3_file):
        self._sql3_file = sqlite3_file

    def compair(self):
        conn = sqlite3.connect(self._sql3_file)
        c = conn.cursor()
        try:
            c.execute("SELECT HID,PF from s_hidandpkg")
        except sqlite3.OperationalError as e:
            print u"执行SELECT s_hidandpkg时发生错误{0}".format(e)
        res = c.fetchall()
        array_for_sysceo = {}
        for row in res:
            key = row[0] + "," + row[1]
            if key in array_for_sysceo:
                array_for_sysceo[key] = array_for_sysceo[key] + 1;
            else:
                array_for_sysceo[key] = 1
        print u"total count (sysceo) {0}".format(len(res))
        try:
            c.execute("SELECT HID,PF from s_hidandpkg_fi")
        except sqlite3.OperationalError as e:
            print u"执行SELECT s_hidandpkg_fi时发生错误{0}".format(e)
        res = c.fetchall()
        array_for_inf = {}
        for row in res:
            key = row[0] + "," + row[1]
            if key in array_for_inf:
                array_for_inf[key] = array_for_inf[key] + 1
            else:
                array_for_inf[key] = 1
        print u"total count (inf) {0}".format(len(res))
        conn.close()
        print u"-------------------我是华丽的分割线-------------------"
        print u"在sysceo中但是不在inf中:"
        cnt = 0
        for k in array_for_sysceo.keys():
            if k not in array_for_inf:
                print k
                cnt = cnt + 1
        print u"总数:",cnt
        print u"-------------------我是华丽的分割线-------------------"
        print u"在inf中但不在sysceo中:"
        cnt = 0
        for k in array_for_inf.keys():
            if k not in array_for_sysceo:
                print k
                cnt = cnt + 1
        print u"总数:", cnt
        return True


def compair_data_tables(sqlite3_file):
    if sqlite3_file is None:
        raise Exception("SQLITE3 file Must be set.")
    else:
        if not os.path.exists(sqlite3_file):
            print "SQLITE3 file not exists"
            return
        sql_cmp = SQLite3Compire(sqlite3_file)
    sql_cmp.compair()
    return


if __name__ == '__main__':
    u"""
    这个脚本用于将scindex转换为SQLITE数据库。
    """

    work_dir = "H:\\SRS_USB\\SRS"
    archive_folder = "H:\\SRS_USB\\Archive"

    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-a", "--workdir", action="store", type="string", dest="work_dir",
                      help=u"指定工作路径,这个路径默认为" + work_dir)
    parser.add_option("-b", "--scfile", action="store", type="string", dest="sc_file")
    parser.add_option("-c", "--sqlite", action="store", type="string", dest="sqlite_file")
    parser.add_option("-d", "--compair", action="store_true", dest="task_compair")
    parser.add_option("-e", "--general", action="store_true", dest="task_general")
    parser.add_option("-f", "--archive_dir", action="store", type="string", dest="archive_dir",
                      help=u"指定7z文件保存的目录,默认为" + archive_folder)
    (options, args) = parser.parse_args()

    if options.work_dir is not None:
        work_dir = options.work_dir

    if options.archive_dir is not None:
        archive_folder = options.archive_dirs

    if options.task_compair:
        sf = "H:\\SRS_USB\\SRS\\drivers.dat"
        if options.sqlite_file is not None:
            sf = options.sqlite_file
        compair_data_tables(sf)
    elif options.task_general:
        load_driver_items_from_file_to_sqlite3_db_and_combine_records(work_dir, archive_folder)
    else:
        # The default action of this script without any parameter.
        # compair_data_tables(options.sqlite_file)
        load_driver_items_from_file_to_sqlite3_db_and_combine_records(work_dir, archive_folder)

