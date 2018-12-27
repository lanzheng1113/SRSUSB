# -*_coding:gb2312-*-
import os
import sqlite3
import codecs
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
        "primary" : "no"
    },
    "WinVx86.ScIndex" : {
        "d_arch" : "x86",
        "d_os_ver" : "6.0|6.1|6.2|6.3|10.0",
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
            i.inf_arch_tag = arch

            if i.inf_os_version == "":
                i.inf_os_version = default_os_ver

            table_name = "s_hidandpkg"
            if not is_primary:
                table_name = "s_hidandpkg_v"
            insert_str = "INSERT INTO {0} " \
                         "(HID,HIDNAME,PATH,OS,PF,TYPE,DRVVER,DRVDATE) " \
                         "VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')" \
                .format(table_name, i.hardware_id, i.device_describe, relate_path_of_inf, i.inf_os_version, arch,
                        i.device_class_name, i.driver_version, i.driver_release_time)
            try:
                c.execute(insert_str)
            except sqlite3.OperationalError as e:
                print u"执行{0}时发生错误{1}".format(insert_str, e)
        conn.commit()
        print u"插入完成"
        conn.close()
        return True


class SrsTransport:
    __objs_driver_item_primary = {}  # 这个对象将存放到主表
    __objs_driver_item_2nd = {}  # 这个对象将存放到副表
    __work_dir = ""
    __combine_count = 0
    __ignore_count = 0
    __sqlite_file = "drivers.dat"
    __sqlite_file_full_path = ""
    __item_count_in_files = 0
    __insert_count = 0

    def __init__(self, v_work_dir):
        self.__work_dir = v_work_dir

    def dump(self):
        print "count of 1st element: {0}".format(len(self.__objs_driver_item_primary.keys()))
        print "count of 2nd element: {0}".format(len(self.__objs_driver_item_2nd.keys()))
        print "total combined count: {0}".format(self.__combine_count)
        print "total count ignore: {0}".format(self.__ignore_count)
        print "total insert count: {0}".format(self.__insert_count)
        print "total item count in files : {0}".format(self.__item_count_in_files)

    def commit(self):
        self.__sqlite_file_full_path = os.path.join(self.__work_dir, self.__sqlite_file)
        if os.path.exists(self.__sqlite_file_full_path):
            conn = sqlite3.connect(self.__sqlite_file_full_path)
            c = conn.cursor()
            table_name = "s_hidandpkg"
            for k, v in self.__objs_driver_item_primary.items():
                obj_array = v
                for i in obj_array:
                    relate_path_of_inf = i.folder + "\\" + i.inf_relate_path
                    insert_str = "INSERT INTO {0} " \
                                 "(HID,HIDNAME,PATH,OS,PF,TYPE,DRVVER,DRVDATE) " \
                                 "VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')" \
                        .format(table_name, i.hardware_id, i.device_describe, relate_path_of_inf, i.inf_os_version,
                                i.inf_arch_tag, i.device_class_name, i.driver_version, i.driver_release_time)
                    try:
                        c.execute(insert_str)
                        self.__insert_count = self.__insert_count + 1
                    except sqlite3.OperationalError as e:
                        print u"执行{0}时发生错误{1}".format(insert_str, e)
            table_name = "s_hidandpkg_v"
            for k, v in self.__objs_driver_item_2nd.items():
                obj_array = v
                for i in obj_array:
                    relate_path_of_inf = i.folder + "\\" + i.inf_relate_path
                    insert_str = "INSERT INTO {0} " \
                                 "(HID,HIDNAME,PATH,OS,PF,TYPE,DRVVER,DRVDATE) " \
                                 "VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')" \
                        .format(table_name, i.hardware_id, i.device_describe, relate_path_of_inf, i.inf_os_version,
                                i.inf_arch_tag, i.device_class_name, i.driver_version, i.driver_release_time)
                    try:
                        c.execute(insert_str)
                        self.__insert_count = self.__insert_count + 1
                    except sqlite3.OperationalError as e:
                        print u"执行{0}时发生错误{1}".format(insert_str, e)
            conn.commit()
            print u"插入完成"
            conn.close()

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
            dr = DriverItem(line)
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
                arch = "ia64"
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
                    print u"跳过错误的项[{0}]-[{1}]-[{2}],文件{3}"\
                        .format(i.hardware_id, relate_path_of_inf, i.inf_arch_tag, sc_index_full_path)
                    self.__ignore_count = self.__ignore_count + 1
                    continue
            else:
                # 自带arch, 但是arch的名字和配置的名字相反。我们需要输出警告
                inf_full_path = os.path.join(self.__work_dir, relate_path_of_inf)
                if i.inf_arch_tag == "x86" and -1 != i.folder.find("x64"):
                    print u"检查可疑项[{0}]-[{1}]-[{2}],在文件{3}".format(i.hardware_id, relate_path_of_inf, i.inf_arch_tag,
                                                             sc_index_full_path)
                    if not self.__inf_check(inf_full_path, "x86"):
                        print u"跳过架构设置(arch)可能有问题的项"
                        self.__ignore_count = self.__ignore_count + 1
                        continue
                    else:
                        print u"通过检测。"
                if i.inf_arch_tag == "x64" and -1 != i.folder.find("x86"):
                    print u"[{0}]-[{1}]-[{2}],在文件{3}".format(i.hardware_id, relate_path_of_inf, i.inf_arch_tag,
                                                             sc_index_full_path)
                    if not self.__inf_check(inf_full_path, "x64"):
                        print u"跳过架构设置(arch)可能有问题的项"
                        self.__ignore_count = self.__ignore_count + 1
                        continue
                    else:
                        print u"通过检测。"
            # 这里是更换系统版本，文本中有空，我们写入数据库的时候不能为空。这个值可以是多个系统版本号的联合
            # 如 : 5.1|5.2|6.0|6.1|6.2|6.3|10.0
            if i.inf_os_version == "":
                i.inf_os_version = default_os_ver
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

    def __inf_check(self, inf_file_path, arch_to_check):
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



class SQLite3DBTrans:
    u"""
    处理去重和合并
    """
    def __init__(self,v_sqlite_file):
        self.__sql_file = v_sqlite_file

    def sqlite3_db_erase_repeat_records(self):
        return

    def sqlite3_db_combine_records(self):
        return


def load_driver_items_from_files_to_sqlite3_db(v_work_dir, v_sqlite_file):
    for k, j in config.items():
        fn = k
        default_arch = j["d_arch"]
        default_os_ver = j["d_os_ver"]
        if j["primary"] == "yes":
            is_primary = True
        else:
            is_primary = False
            print u"插入表2"
        sct = SrsTrans(v_work_dir, fn)
        if v_sqlite_file is not None:
            sct.set_sqlite_file(v_sqlite_file)
        if not sct.tran(default_arch, default_os_ver, is_primary):
            print u"转换失败"
        else:
            print u"转换成功"
    return


def load_driver_items_from_file_to_sqlite3_db_and_combine_records(v_work_dir):
    sct = SrsTransport(v_work_dir)
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
    sct.commit()
    sct.dump()
    return


if __name__ == '__main__':
    u"""
    这个脚本用于将scindex转换为SQLITE数据库。
    """
    work_dir = "H:\\SRS_USB\\SRS"
    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-a", "--workdir", action="store", type="string", dest="work_dir",
                      help=u"指定工作路径,这个路径默认为" + work_dir)
    parser.add_option("-b", "--scfile", action="store", type="string", dest="sc_file")
    parser.add_option("-c", "--sqlite", action="store", type="string", dest="sqlite_file")
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
    # load_driver_items_from_files_to_sqlite3_db(work_dir, options.qlite_file)
    load_driver_items_from_file_to_sqlite3_db_and_combine_records(work_dir)

