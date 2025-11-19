from pprint import pformat

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer

import ainakan

print("Local parameters:", highlight(pformat(ainakan.query_system_parameters()), PythonLexer(), Terminal256Formatter()))
print(
    "USB device parameters:",
    highlight(pformat(ainakan.get_usb_device().query_system_parameters()), PythonLexer(), Terminal256Formatter()),
)
