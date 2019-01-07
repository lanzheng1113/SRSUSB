#include <windows.h>
#include <stdio.h>
#include "sqlite3/CppSQLite3.h"
#include <string>
using std::string;
#include <vector>
using std::vector;
#include <sstream>
using std::stringstream;
#include "util/stringex.h"
#include "util/StringList.h"

#ifdef _DEBUG
#pragma comment(lib,"WZTKCommonMTd.lib")
#else
#pragma comment(lib,"WZTKCommonMt.lib")
#endif // _DEBUG


struct QUERY_RESULT
{
	string path;
	string os;
	string version;
	string date;
};

int main(int argc, char** argv)
{
	if (argc != 4)
	{
		return 1;
	}

	string pHID = argv[1];
	if (pHID.empty())
	{
		return 2;
	}
	string pPF = argv[2];
	if (pPF != "x64" && pPF != "x86")
	{
		return 3;
	}
	string pOS = argv[3];
	if (pOS != "5.1" && pOS != "5.2" && pOS != "6.0"
		&& pOS != "6.1" && pOS != "6.2" && pOS != "6.3"
		&& pOS != "10.0")
	{
		return 4;
	}

	CppSQLite3DB sql3db;
	try
	{
		sql3db.open("H:\\SRS_USB\\SRS\\drivers.dat");
		char* szkey = "www.hanboshi.com";
		sql3db.key(szkey,strlen(szkey));
		vector<QUERY_RESULT> vqr;
		vector<QUERY_RESULT> aqr;
		stringstream ss;
		ss << "SELECT * FROM \"s_hidandpkg\" WHERE HID = \""
			<< pHID
			<< "\" and PF=\""
			<< pPF
			<< "\"";

		CppSQLite3Query query = sql3db.execQuery(ss.str().c_str());
		while (!query.eof())
		{
			const char* pTemp = NULL;
			QUERY_RESULT qr;
			pTemp = query.getStringField("PATH");
			qr.path = pTemp ? pTemp : "";
			pTemp = query.getStringField("OS");
			qr.os = pTemp ? pTemp : "";
			pTemp = query.getStringField("DRVVER");
			qr.version = pTemp ? pTemp : "";
			pTemp = query.getStringField("DRVDATE");
			qr.date = pTemp ? pTemp : "";

			if (qr.path.empty() || qr.os.empty() || qr.version.empty() || qr.date.empty())
			{
				query.nextRow();
				continue;
			}
			aqr.push_back(qr);
			String str = qr.os;
			StringList loo = str.split("|");
			for (auto i : loo)
			{
				if (i == pOS)
				{
					vqr.push_back(qr);
					break;
				}
			}
			query.nextRow();
		}
		
		sql3db.close();

		int c = 0;
		for (auto i : vqr)
		{
			printf("------------------%d---------------\n",++c);
			printf("PATH:%s\n", i.path.c_str());
			printf("OS  :%s\n", i.os.c_str());
			printf("VER :%s\n", i.version.c_str());
			printf("DATE:%s\n", i.date.c_str());
		}
	}
	catch (CppSQLite3Exception& e)
	{
		printf("CppSQLite3Exception:%s\n", e.errorMessage());
	}

	system("pause");
	return 0;
}
