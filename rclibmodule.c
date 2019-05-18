// Taken from https://docs.python.org/3.7/extending/newtypes_tutorial.html
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "RadioControlProtocolC/rc_lib.h"

typedef struct {
    PyObject_HEAD
    rc_lib_package_t pkg;
} RcLibObject;

static int rclib_init(RcLibObject *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = {"resolution", "channel_count", NULL};
    int res = 0, channel_count  = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|HH", kwlist, &res, &channel_count)) {
        return -1;
    }
    rc_lib_init_tx(&self->pkg, res, channel_count);

    return 0;
}

static PyObject* rclib_encode(RcLibObject *self, PyObject *value, void *closure) {
    uint16_t len = rc_lib_encode(&self->pkg);
    return Py_BuildValue("y#", self->pkg.buffer, len);
}

static PyObject* rclib_decode(RcLibObject *self, PyObject *args, void *closure) {
    uint8_t byte;
    if (!PyArg_ParseTuple(args, "b", &byte)) {
        return NULL;
    }

    bool result = rc_lib_decode(&self->pkg, byte);
    return Py_BuildValue("p", result);
}

static PyMethodDef methods[] = {
        {"encode", (PyCFunction) rclib_encode, METH_NOARGS, "Serialize the data"},
        {"decode", (PyCFunction) rclib_decode, METH_VARARGS, "Serialize the data"},
        {NULL}  /* Sentinel */
};


static PyTypeObject RcLibType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "rclib.pkg",
        .tp_doc = "RcLib Package",
        .tp_basicsize = sizeof(RcLibObject),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_new = PyType_GenericNew,
        .tp_init = (initproc) rclib_init,
        .tp_methods = methods
};

static PyModuleDef RcLibModule = {
        PyModuleDef_HEAD_INIT,
        .m_name = "rclib",
        .m_doc = "rclib module",
        .m_size = -1
};

PyMODINIT_FUNC
PyInit_rclib(void)
{
    PyObject *m;
    if (PyType_Ready(&RcLibType) < 0)
        return NULL;

    m = PyModule_Create(&RcLibModule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&RcLibType);
    PyModule_AddObject(m, "Pkg", (PyObject *) &RcLibType);
    return m;
}