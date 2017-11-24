# encoding: utf-8
import sys
import cStringIO
import dis
import marshal

def reload2(target_module_obj):
    print 'import {}'.format(target_module_obj.__name__)
    reload(target_module_obj)

    with open(target_module_obj.__file__, 'rb') as f:
        f.read(8)
        module_code = marshal.load(f)

    stdout = cStringIO.StringIO()
    sys.stdout = stdout
    dis.disassemble(module_code)
    sys.stdout = sys.__stdout__

    assembly_str = stdout.getvalue()
    stdout.close()

    print assembly_str

import lib
reload2(lib)
