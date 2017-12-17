# encoding: utf-8

def reload1(target_module_obj):
    reload(target_module_obj)
    with open(target_module_obj.__file__, 'r') as f:
        module_source = f.read()

    local_symbols = {}
    exec(module_source, target_module_obj.__dict__, local_symbols)
    for k,v in local_symbols.items():
        target_module_obj.__dict__[k] = v

import re

def find_symbols(module_obj):
    target_reg = re.compile('^\s*?from ([A-Za-z\.].+?) import (.+?)$')
    with open(module_obj.__file__, 'r') as f:
        for line in f:
            m = target_reg.match(line)
            if m is None:
                continue
            module_name = m.group(1)
            symbol_names = m.group(2)
            print 'from {} import {}'.format(module_name, symbol_names)

import lib
print lib.lib2_f1
reload1(lib)
print lib.lib2_f1

find_symbols(lib)

