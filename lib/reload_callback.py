# encoding: utf-8
import imp
import sys

def add_callback(filepath, callback):
    ReloadCallback.add(filepath, callback)

class ReloadCallback(object):

    __hook = None
    __callbacks = {}

    @staticmethod
    def add(filepath, callback):
        print '{} -> {}'.format(filepath, callback)
        if ReloadCallback.__hook is None:
            hook = ReloadCallback()
            sys.meta_path.append(hook)
            ReloadCallback.__hook = hook

        ReloadCallback.__callbacks[filepath] = callback

    def find_module(self, _1, _2):
        return self

    def load_module(self, fullname):
        if fullname not in sys.modules:
            return None

        module_obj = sys.modules[fullname]
        filepath = module_obj.__file__

        callbacks = ReloadCallback.__callbacks
        if filepath not in callbacks:
            return None

        print 'load_module({})'.format(fullname)
        module_obj = imp.reload(sys.modules[fullname])

        filepath = module_obj.__file__

        callback = callbacks[filepath]
        callback(module_obj)

        return module_obj
