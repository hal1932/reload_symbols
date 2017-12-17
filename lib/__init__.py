# encoding: utf-8

import libsrc1
from libsrc2 import *
from libsrc3 import lib3_f1, lib3_f2
from libsrc4 import *

def test():
    lib2_f1()

def __on_reload(module_obj):
    import sys
    m = sys.modules['lib.libsrc2']
    print m
    reload(m)
    print 'on_reload', module_obj
    print '{} -> {}'.format(module_obj.__dict__['lib2_f1'], m.__dict__['lib2_f1'])
    module_obj.__dict__['lib2_f1'] = m.__dict__['lib2_f1']

import reload_callback as rc
rc.add_callback(__file__, __on_reload)
