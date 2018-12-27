# -*_coding:gb2312-*-
import os
import shutil
import subprocess
import codecs
import datetime
import sqlite3
from optparse import OptionParser


config = {
    "Allx64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "5.1|5.2|6.0|6.1|6.2|6.3|10",
        "primary" : "yes"
    },
    "Allx86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "5.1|5.2|6.0|6.1|6.2|6.3|10",
        "primary" : "yes"
    },
    "Nt6x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.0|6.1|6.2|6.3|10",
        "primary" : "yes"
    },
    "Nt6x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.0|6.1|6.2|6.3|10",
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
        "d_os_ver" : "10",
        "primary" : "yes"
    },
    "Win10x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "10",
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
        "d_os_ver" : "6.3|10",
        "primary" : "yes"
    },
    "Win8110x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.3|10",
        "primary" : "yes"
    },
    "Win88110x64.ScIndex" : {
        "d_arch" : "x64",
        "d_os_ver" : "6.2|6.3|10",
        "primary" : "yes"
    },
    "Win88110x86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.2|6.3|10",
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
        "d_os_ver" : "6.0|6.1|6.2|6.3|10",
        "primary" : "no"
    },
    "WinVx86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.0|6.1|6.2|6.3|10",
        "primary" : "no"
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

    def __init__(self, string_device):
        sl = string_device.split('|')
        if len(sl) <= 1:
            self.is_valid = False
            return
        if len(sl) != 17:
            print "Bad line [{0}],cnt={1}".format(string_device,len(sl))
            return
        self.hardware_id = sl[1]
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


class SrsTrans:
    u"""
    转换文本类型的配置到sqlite数据库
    """
    __work_dir = ""
    __sc_index = ""
    __sqlite_file = "drivers.dat"
    __sc_full_path = ""
    __sqlite_file_full_path = ""

    def __init__(self, v_work_dir, v_sc_index):
        self.__work_dir = v_work_dir
        self.__sc_index = v_sc_index

    def set_work_dir(self, v_work_dir):
        self.__work_dir = v_work_dir

    def set_sc_index(self, v_sc_index):
        self.__sc_index = v_sc_index

    def set_sqlite_file(self, v_sqlite_file):
        self.__sqlite_file = v_sqlite_file

    def tran(self, default_arch, default_os_ver, is_primary):
        self.__sc_full_path = os.path.join(self.__work_dir, self.__sc_index)
        if not os.path.exists(self.__sc_full_path):
            print u"需要处理的sc文件并不存在！"
            return False
        self.__sqlite_file_full_path = os.path.join(self.__work_dir, self.__sqlite_file)
        if not os.path.exists(self.__sqlite_file_full_path):
            print u"目的SQLITE文件并不存在！"
            return False
        print u"开始处理文件{0}并保存到{1}".format(self.__sc_full_path, self.__sqlite_file_full_path)
        file_object = open(self.__sc_full_path, 'r')
        inf_object_array = []
        for line in file_object:
            line = line.strip('\r')
            line = line.strip('\n')
            dr = DriverItem(line)
            if dr.is_valid:
                inf_object_array.append(dr)
        file_object.close()

        conn = sqlite3.connect(self.__sqlite_file_full_path)
        c = conn.cursor()
        for i in inf_object_array:
            relate_path_of_inf = i.folder + "\\" + i.inf_relate_path
            temp_str = i.inf_arch_tag.upper()
            # if "NTAMD64" != temp_str and "NTX86" != temp_str and "NTIA64" != temp_str:
            #    print "Bad record."
            #    continue
            arch = ""
            if "NTAMD64" == temp_str:
                arch = "x64"
            elif "NTX86" == temp_str:
                arch = "x86"
            elif "NTIA64" == temp_str:
                arch = "ia64"
            else:
                arch = default_arch

            if i.inf_os_version == "":
                i.inf_os_version = default_os_ver

            table_name = "s_hidandpkg"
            if is_primary != True:
                table_name = "s_hidandpkg_v"
            insert_str = "INSERT INTO {0} " \
                         "(HID,HIDNAME,PATH,OS,PF,TYPE,DRVVER,DRVDATE) " \
                         "VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')" \
                .format(table_name, i.hardware_id, i.device_describe, relate_path_of_inf, i.inf_os_version, arch,
                        i.device_class_name, i.driver_version, i.driver_release_time)
            try:
                c.execute(insert_str)
            except  sqlite3.OperationalError as e:
                print u"执行{0}时发生错误{1}".format(insert_str, e)
        conn.commit()
        print u"插入完成"
        conn.close()
        return True


def main():
    work_dir = "H:\\SRS_USB\\SRS"
    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-a", "--workdir", action="store", type="string", dest="work_dir",
                      help=u"指定工作路径,这个路径默认为" + work_dir)
    parser.add_option("-b", "--scfile", action="store", type="string", dest="sc_file")
    (options, args) = parser.parse_args()
    if options.work_dir is not None:
        work_dir = options.work_dir
    u"""
    if options.sc_file is None:
        print u"你必须指定要处理的scindex文件"
        return
    sc_file_full_path = os.path.join(work_dir, options.sc_file)
    if not os.path.exists(sc_file_full_path):
        print u"需要处理的sc文件并不存在！"
        return
    """
    fn = ""
    default_arch = ""
    default_os_ver = ""
    is_primary = False
    for k, j in config.items():
        fn = k
        default_arch = j["d_arch"]
        default_os_ver = j["d_os_ver"]
        if j["primary"] == "yes":
            is_primary = True
        else:
            is_primary = False
            print u"插入表2"
        sct = SrsTrans(work_dir, fn)
        if not sct.tran(default_arch, default_os_ver, is_primary):
            print u"转换失败"
        else:
            print u"转换成功"
    return


if __name__ == '__main__':
    u"""
    这个脚本用于将scindex转换为SQLITE数据库。
    """
    main()

