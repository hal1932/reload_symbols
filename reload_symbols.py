# encoding: utf-8
import sys
import inspect
import ast

def reload_symbols(target_module_obj):
    print 'import {}'.format(target_module_obj.__name__)
    reload(target_module_obj)

    for module_obj, symbol_names in __find_symbols(target_module_obj).items():
        print 'from {} import {}'.format(module_obj.__name__, ', '.join(symbol_names))
        reload(module_obj)
        for symbol_name in symbol_names:
            print '  {}.{}: {} -> {}'.format(
                target_module_obj.__name__, symbol_name,
                module_obj.__dict__[symbol_name], target_module_obj.__dict__[symbol_name])
            target_module_obj.__dict__[symbol_name] = module_obj.__dict__[symbol_name]

def __find_symbols(module_obj):
    result = {}

    source = inspect.getsource(module_obj)
    tree = ast.parse(source)

    for node in tree.body:
        if node.__class__ != ast.ImportFrom:
            continue

        module_name = '{}.{}'.format(module_obj.__name__, node.module)
        target_module = sys.modules[module_name]

        symbol_names = [x.name for x in node.names]
        if symbol_names[0] == '*':
            if '__all__' in target_module.__dict__:
                symbol_names = target_module.__dict__['__all__']
            else:
                symbol_names = [x for x in target_module.__dict__ if not x.startswith('__')]

        result[target_module] = symbol_names

    return result

import lib
reload_symbols(lib)
