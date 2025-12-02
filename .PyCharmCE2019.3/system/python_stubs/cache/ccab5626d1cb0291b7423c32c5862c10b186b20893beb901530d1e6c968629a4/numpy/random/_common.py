# encoding: utf-8
# module numpy.random._common
# from C:\Users\Lenovo\Desktop\project\SyntheticIdCardPy\venv\lib\site-packages\numpy\random\_common.cp37-win_amd64.pyd
# by generator 1.147
# no doc

# imports
import builtins as __builtins__ # <module 'builtins' (built-in)>
import sys as sys # <module 'sys' (built-in)>
import numpy as np # C:\Users\Lenovo\Desktop\project\SyntheticIdCardPy\venv\lib\site-packages\numpy\__init__.py

# functions

# Error generating skeleton for function namedtuple: Function has keyword-only parameters or annotations, use getfullargspec() API which can support them

# classes

class interface(tuple):
    """ interface(state_address, state, next_uint64, next_uint32, next_double, bit_generator) """
    def _asdict(self): # reliably restored by inspect
        """ Return a new OrderedDict which maps field names to their values. """
        pass

    @classmethod
    def _make(cls, *args, **kwargs): # real signature unknown
        """ Make a new interface object from a sequence or iterable """
        pass

    def _replace(_self, **kwds): # reliably restored by inspect
        """ Return a new interface object replacing specified fields with new values """
        pass

    def __getnewargs__(self): # reliably restored by inspect
        """ Return self as a plain tuple.  Used by copy and pickle. """
        pass

    def __init__(self, state_address, state, next_uint64, next_uint32, next_double, bit_generator): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(_cls, state_address, state, next_uint64, next_uint32, next_double, bit_generator): # reliably restored by inspect
        """ Create new instance of interface(state_address, state, next_uint64, next_uint32, next_double, bit_generator) """
        pass

    def __repr__(self): # reliably restored by inspect
        """ Return a nicely formatted representation string """
        pass

    bit_generator = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Alias for field number 5"""

    next_double = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Alias for field number 4"""

    next_uint32 = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Alias for field number 3"""

    next_uint64 = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Alias for field number 2"""

    state = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Alias for field number 1"""

    state_address = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Alias for field number 0"""


    _fields = (
        'state_address',
        'state',
        'next_uint64',
        'next_uint32',
        'next_double',
        'bit_generator',
    )
    _fields_defaults = {}
    _field_defaults = {}
    __slots__ = ()


# variables with complex values

__all__ = [
    'interface',
]

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x000001637FCE5DC8>'

__pyx_capi__ = {
    'LEGACY_POISSON_LAM_MAX': None, # (!) real value is '<capsule object "double" at 0x000001637FCE2240>'
    'MAXSIZE': None, # (!) real value is '<capsule object "uint64_t" at 0x000001637FCE2270>'
    'POISSON_LAM_MAX': None, # (!) real value is '<capsule object "double" at 0x000001637FCE2210>'
    'benchmark': None, # (!) real value is '<capsule object "PyObject *(bitgen_t *, PyObject *, Py_ssize_t, PyObject *)" at 0x000001637FCE22A0>'
    'check_array_constraint': None, # (!) real value is '<capsule object "int (PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)" at 0x000001637FCE2390>'
    'check_constraint': None, # (!) real value is '<capsule object "int (double, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)" at 0x000001637FCE2360>'
    'cont': None, # (!) real value is '<capsule object "PyObject *(void *, void *, PyObject *, PyObject *, int, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *)" at 0x000001637FCE2510>'
    'cont_broadcast_3': None, # (!) real value is '<capsule object "PyObject *(void *, void *, PyObject *, PyObject *, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)" at 0x000001637FCE25A0>'
    'cont_f': None, # (!) real value is '<capsule object "PyObject *(void *, bitgen_t *, PyObject *, PyObject *, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *)" at 0x000001637FCE2570>'
    'disc': None, # (!) real value is '<capsule object "PyObject *(void *, void *, PyObject *, PyObject *, int, int, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)" at 0x000001637FCE2540>'
    'discrete_broadcast_iii': None, # (!) real value is '<capsule object "PyObject *(void *, void *, PyObject *, PyObject *, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)" at 0x000001637FCE25D0>'
    'double_fill': None, # (!) real value is '<capsule object "PyObject *(void *, bitgen_t *, PyObject *, PyObject *, PyObject *)" at 0x000001637FCE23F0>'
    'float_fill': None, # (!) real value is '<capsule object "PyObject *(void *, bitgen_t *, PyObject *, PyObject *, PyObject *)" at 0x000001637FCE2420>'
    'float_fill_from_double': None, # (!) real value is '<capsule object "PyObject *(void *, bitgen_t *, PyObject *, PyObject *, PyObject *)" at 0x000001637FCE2450>'
    'int_to_array': None, # (!) real value is '<capsule object "PyArrayObject *(PyObject *, PyObject *, PyObject *, PyObject *)" at 0x000001637FCE24B0>'
    'kahan_sum': None, # (!) real value is '<capsule object "double (double *, npy_intp)" at 0x000001637FCE23C0>'
    'prepare_cffi': None, # (!) real value is '<capsule object "PyObject *(bitgen_t *)" at 0x000001637FCE2300>'
    'prepare_ctypes': None, # (!) real value is '<capsule object "PyObject *(bitgen_t *)" at 0x000001637FCE2330>'
    'random_raw': None, # (!) real value is '<capsule object "PyObject *(bitgen_t *, PyObject *, PyObject *, PyObject *)" at 0x000001637FCE22D0>'
    'validate_output_shape': None, # (!) real value is '<capsule object "PyObject *(PyObject *, PyArrayObject *)" at 0x000001637FCE24E0>'
    'wrap_int': None, # (!) real value is '<capsule object "PyObject *(PyObject *, PyObject *)" at 0x000001637FCE2480>'
}

__spec__ = None # (!) real value is "ModuleSpec(name='numpy.random._common', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x000001637FCE5DC8>, origin='C:\\\\Users\\\\Lenovo\\\\Desktop\\\\project\\\\SyntheticIdCardPy\\\\venv\\\\lib\\\\site-packages\\\\numpy\\\\random\\\\_common.cp37-win_amd64.pyd')"

__test__ = {}

