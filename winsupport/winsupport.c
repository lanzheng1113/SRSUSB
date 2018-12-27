// spam.c
#include "Python.h"

static PyObject *SpamError;
int __stdcall get_file_machine_bit(const char * szFullPath);
static PyObject *py_is64PEFile(PyObject *self, PyObject *args)
{
	const char *file_path;
	int sts;

	if (!PyArg_ParseTuple(args, "s", &file_path))
		return NULL;
	
	sts = get_file_machine_bit(file_path);
	if (sts < 0) {
		PyErr_SetString(SpamError, "Get file machine bit failed");
		return NULL;
	}
	if (sts == 32)
	{
		return PyLong_FromLong(0);
	}
	else
		return PyLong_FromLong(1);
}

static PyMethodDef SpamMethods[] = {
	{ "is_pe_64",  py_is64PEFile, METH_VARARGS,
	"Check a file is x64" },
	{ NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC
initwinsupport(void)
{
	PyObject *m;
	m = Py_InitModule("winsupport", SpamMethods);
	if (m == NULL)
		return;
	SpamError = PyErr_NewException("winsupport.error", NULL, NULL);
	Py_INCREF(SpamError);
	PyModule_AddObject(m, "error", SpamError);
}

