# encoding: utf-8

def reload1(target_module_obj):
    reload(target_module_obj)
    with open(target_module_obj.__file__, 'r') as f:
        module_source = f.read()
    exec(module_source, target_module_obj.__dict__, {})

import lib
print lib.lib2_f1
reload1(lib)
print lib.lib2_f1

