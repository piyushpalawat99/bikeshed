# coding: utf-8
from requests.compat import is_py3


try:
    import io
except ImportError:
    import io as StringIO

try:
    from io import StringIO as cStringIO
except ImportError:
    cStringIO = None

if is_py3:
    def u(s):
        return s
else:
    def u(s):
        return s.decode('unicode-escape')
