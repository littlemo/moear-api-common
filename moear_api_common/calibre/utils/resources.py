#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import with_statement

__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'


import builtins

from ...calibre import config_dir

#_resolver = PathResolver()

def get_path(path, data=False, allow_user_override=True):
    #fpath = _resolver(path, allow_user_override=allow_user_override)
    fpath = path
    if data:
        with open(fpath, 'rb') as f:
            return f.read()
    return fpath

def get_image_path(path, data=False, allow_user_override=True):
    if not path:
        return get_path('images')
    return get_path('images/'+path, data=data)

builtins.__dict__['P'] = get_path
builtins.__dict__['I'] = get_image_path
