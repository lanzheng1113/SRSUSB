﻿这个模块是SQLITE3静态库，支持带密码访问。


一. 编译加密的Sqlite3
1. 下载wxSqlite3-1.9.9.zip后,解压到wxsqlite3-1.9.9
(http://sourceforge.net/projects/wxcode/files/Components/)
2. 下载www.Sqlite.org的sqlite-amalgamation-3_XXXX.zip,将压缩包中的文件全部提取到 wxsqlite3-1.9.9\sqlite3\secure\src\codec-c 下(写这篇文章时用的版本是3.6.23.1).
编辑 sqlite3.def , 添加 下面两个函数导出
    sqlite3_rekey
    sqlite3_key
3. 打开VS,新建一个"static lib",工程名为"Sqlite3Encrypt",保存到"wxsqlite3-1.9.9\sqlite3"下.
4. 导入文件:只要单纯的导入 sqlite3secure.c 这个文件就好了.
5. 设置工程属性: (为方便使用 将Sqlite3的输出调整到wxSqlite3工程的输出目录中).在这一步中,分为Debug与Release版.( 可以通过新建工程时建一个DLL工程,这样就内置了两个版本的配置,然后再将"常规->配置类型"设置为"静态库(lib)"就可以了.)
常规->输出目录:
        "..\..\lib\vc_lib"
C/C++->预处理->预处理器定义:
        SQLITE3ENCRYPT_EXPORTS
        SQLITE_ENABLE_FTS3
        SQLITE_ENABLE_FTS3_PARENTHESIS
        SQLITE_ENABLE_RTREE
        SQLITE_SECURE_DELETE
        SQLITE_SOUNDEX
        SQLITE_ENABLE_COLUMN_METADATA
        SQLITE_HAS_CODEC
        CODEC_TYPE=CODEC_TYPE_AES128
C/C++->输出文件->程序数据库文件名:
        "..\..\lib\vc_lib\Sqlite3EncryptD.pdb" //Debug版
       "..\..\lib\vc_lib\Sqlite3Encrypt.pdb"   //Release版
管理员->输出文件:
        $(OutDir)\$(ProjectName)D.lib //Debug版
        $(OutDir)\$(ProjectName).lib    //Release版
6. 编译生成 Sqlite3EncryptD.lib,Sqlite3Encrypt.lib

release x86 C++ 代码生成 要用MTD编译

release x86 C++ 代码生成 要用MT编译