#include <windows.h>
#include <stdio.h>
int __stdcall get_file_machine_bit(const char * szFullPath)
{
	FILE * peFile = NULL;
	fopen_s(&peFile, szFullPath, "rb");
	if (peFile == NULL)
	{
		fclose(peFile);
		return -1;
	}

	IMAGE_DOS_HEADER imageDosHeader;
	fread(&imageDosHeader, sizeof(IMAGE_DOS_HEADER), 1, peFile);
	if (imageDosHeader.e_magic != IMAGE_DOS_SIGNATURE)
	{
		fclose(peFile);
		return -1;
	}

	IMAGE_NT_HEADERS imageNtHeaders;
	fseek(peFile, imageDosHeader.e_lfanew, SEEK_SET);
	fread(&imageNtHeaders, sizeof(IMAGE_NT_HEADERS), 1, peFile);
	fclose(peFile);
	if (imageNtHeaders.Signature != IMAGE_NT_SIGNATURE)
	{
		return -1;
	}

	if (imageNtHeaders.FileHeader.Machine == IMAGE_FILE_MACHINE_I386)
	{
		return 32;
	}
	if (imageNtHeaders.FileHeader.Machine == IMAGE_FILE_MACHINE_IA64 ||
		imageNtHeaders.FileHeader.Machine == IMAGE_FILE_MACHINE_AMD64)
	{
		return 64;
	}

	return -1;
}
