# encoding: utf-8
import sys
import inspect
import ast

def reload_symbols(target_module_obj):
    print 'import {}'.format(target_module_obj.__name__)
    reload(target_module_obj)

    source = inspect.getsource(target_module_obj)
    tree = ast.parse(source)
    for node in tree.body:
        if node.__class__ == ast.ImportFrom:
            module_name = '{}.{}'.format(target_module_obj.__name__, node.module)
            target_module = sys.modules[module_name]

            symbol_names = [x.name for x in node.names]
            if symbol_names[0] == '*':
                symbol_names = [x for x in target_module.__dict__ if not x.startswith('__')]

            print 'from {} import {}'.format(node.module, node.names[0].name)
            reload(target_module)
            for symbol_name in symbol_names:
                target_module_obj.__dict__[symbol_name] = target_module.__dict__[symbol_name]
