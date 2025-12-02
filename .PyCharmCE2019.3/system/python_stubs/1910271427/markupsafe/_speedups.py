# encoding: utf-8
# module markupsafe._speedups
# from C:\Users\Lenovo\Desktop\project\SyntheticIdCardPy\venv\lib\site-packages\markupsafe\_speedups.cp37-win_amd64.pyd
# by generator 1.147
# no doc
# no imports

# functions

def escape(*args, **kwargs): # real signature unknown
    """
    Replace the characters ``&``, ``<``, ``>``, ``'``, and ``"`` in the string with HTML-safe sequences. Use this if you need to display text that might contain such characters in HTML.
    
    If the object has an ``__html__`` method, it is called and the return value is assumed to already be safe for HTML.
    
    :param s: An object to be converted to a string and escaped.
    :return: A :class:`Markup` string with the escaped text.
    """
    pass

def escape_silent(None_): # real signature unknown; restored from __doc__
    """
    Like :func:`escape` but treats ``None`` as the empty string. Useful with optional values, as otherwise you get the string ``'None'`` when the value is ``None``.
    
    >>> escape(None)
    Markup('None')
    >>> escape_silent(None)
    Markup('')
    """
    pass

def soft_str(value): # real signature unknown; restored from __doc__
    """
    Convert an object to a string if it isn't already. This preserves a :class:`Markup` string rather than converting it back to a basic string, so it will still be marked as safe and won't be escaped again.
    
    >>> value = escape("<User 1>")
    >>> value
    Markup('&lt;User 1&gt;')
    >>> escape(str(value))
    Markup('&amp;lt;User 1&amp;gt;')
    >>> escape(soft_str(value))
    Markup('&lt;User 1&gt;')
    """
    pass

# no classes
# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x000001DC1C8064C8>'

__spec__ = None # (!) real value is "ModuleSpec(name='markupsafe._speedups', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x000001DC1C8064C8>, origin='C:\\\\Users\\\\Lenovo\\\\Desktop\\\\project\\\\SyntheticIdCardPy\\\\venv\\\\lib\\\\site-packages\\\\markupsafe\\\\_speedups.cp37-win_amd64.pyd')"

