__license__   = 'GPL v3'
__copyright__ = '2008, Kovid Goyal kovid@kovidgoyal.net'
__docformat__ = 'restructuredtext en'

'''
Perform various initialization tasks.
'''

import locale, sys, os, re

# Default translation is NOOP
import builtins
builtins.__dict__['_'] = lambda s: s

# For strings which belong in the translation tables, but which shouldn't be
# immediately translated to the environment language
builtins.__dict__['__'] = lambda s: s
builtins.__dict__['P'] = lambda s: s
builtins.__dict__['I'] = lambda s: s
builtins.__dict__['lopen'] = open
builtins.__dict__['icu_lower'] = lambda x:x.lower()
builtins.__dict__['icu_upper'] = lambda x:x.upper()
builtins.__dict__['icu_title'] = lambda x:x.capitalize()
builtins.__dict__['dynamic_property'] = lambda func: func(None)

from ..calibre.constants import *

_run_once = False
winutil = winutilerror = None
_base_dir = "."

if not _run_once:
    _run_once = True

