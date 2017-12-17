# encoding: utf-8
import ast
import imp
import inspect
import sys

class ReloadSymbolsHook(object):

    def __init__(self, target_module_obj):
        self.__target_module_obj = target_module_obj

    def find_module(self, fullname, _):
        if fullname != self.__target_module_obj.__name__:
            return None

        return self

    def load_module(self, _):
        target_module_obj = imp.reload(self.__target_module_obj)
        target_symbols = self.__find_symbols(target_module_obj)

        for module_obj, symbol_names in target_symbols.items():
            # print 'from {} import {}'.format(module_obj.__name__, ', '.join(symbol_names))
            module_obj = imp.reload(module_obj)
            for symbol_name in symbol_names:
                # print '  {}.{}: {} -> {}'.format(
                #     target_module_obj.__name__, symbol_name,
                #     module_obj.__dict__[symbol_name], target_module_obj.__dict__[symbol_name])
                target_module_obj.__dict__[symbol_name] = module_obj.__dict__[symbol_name]

        return target_module_obj

    def __find_symbols(self, module_obj):
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

# import lib
# sys.meta_path.append(ReloadSymbolsHook(lib))
# reload(lib)
