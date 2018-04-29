import os
import csv
import inspect
import tempfile
import subprocess


def pve():
    types_to_exclude = ['module', 'function', 'builtin_function_or_method',
                        'instance', '_Feature', 'type', 'ufunc']
    frame = inspect.currentframe()
    locals_dict = dict(frame.f_back.f_locals)
    handle, fn = tempfile.mkstemp(suffix='.csv')
    with os.fdopen(handle,"w", encoding='utf8',errors='surrogateescape',\
                  newline='') as f:
        w = csv.writer(f)
        for key, value in locals_dict.items():
            var_type = str(type(locals_dict[key]))[8:-2]
            if not key.startswith('_') and var_type not in types_to_exclude:
                if var_type == 'list':
                    row = [key] + [var_type] + value
                elif var_type == 'range':
                    row = [key] + [var_type] + [v for v in value]
                elif var_type == 'numpy.ndarray':
                    row = [key] + [var_type] + list(value)
                else:
                    row = [key] + [var_type] + [value]
                w.writerow(row)
    p = subprocess.Popen(["scim", fn])
    returncode = p.wait()
