# encoding: utf-8
import types
import sys

def reload1(target_module_obj):

    print target_module_obj.__dict__['lib2_f1'], sys.modules['lib.libsrc2'].__dict__['lib2_f1']
    reload(target_module_obj)
    reload(sys.modules['lib.libsrc2'])
    # with open(target_module_obj.__file__, 'r') as f:
    #     module_source = f.read()
    # exec(module_source, target_module_obj.__dict__, target_module_obj.__dict__)
    target_module_obj.__dict__['lib2_f1'] = sys.modules['lib.libsrc2'].__dict__['lib2_f1']

import lib
print lib.lib2_f1
reload1(lib)
#import reload_symbols
#reload_symbols.reload_symbols(lib)
print lib.lib2_f1

