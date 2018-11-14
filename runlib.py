#!/usr/bin/python3
import ctypes
import os
import sys

arg_types = {'int': 'c_int32',
             'long': 'c_long',
             'float': 'c_float',
             'double': 'c_double',
             'char': 'c_char',
             'bool': 'c_bool',
             'buffer': 'c_buffer',
             'byte': 'c_byte',
             'char_p': 'c_char_p',
             'short': 'c_short',
             'ulong': 'c_ulong',
             'ubyte': 'c_ubyte',
             'uint': 'c_uint',
             'ushort': 'c_ushort',
             'void_p': 'c_void_p',
             'wchar': 'c_wchar'}


def get_func(so_filename, func_name):
    if not os.path.exists(so_filename):
        return None, "file {} not exists!".format(so_filename)
    try:
        dll = ctypes.cdll.LoadLibrary(so_filename)
        func = getattr(dll, func_name)
    except OSError as error:
        return None, '{};{} is not a Dynamic Link Library!'.format(error, so_filename)
    except AttributeError as error:
        return None, '{};can not find function {} from {}'.format(error, func_name, so_filename)
    return func, 'OK!'


def parse_restype(args):
    res_type = 'c_int32'
    for arg in range(args.__len__()):
        if args[arg].startswith('--res-type'):
            try:
                res_type = args[arg].split('=')[1]
                if res_type not in arg_types.keys():
                    print('res_type must in {}'.format(arg_types.keys()))
                    exit(0)
                res_type = arg_types.get(res_type, 'c_int32')
                args.remove(args[arg])
                break
            except ValueError:
                usage()
                exit(0)
    return args, res_type


def parse_args(args):
    new_args = []

    def is_number(x):
        try:
            float(x)
            return True
        except ValueError:
            return False
    for arg in args:
        arg_type, arg = arg.split('(')
        arg_type = arg_types.get(arg_type)
        arg = arg[:-1]
        if is_number(arg):
            new_args.append('{}.{}({})'.format('ctypes', arg_type, arg))
        else:
            new_args.append('\"{}\".encode()'.format(arg))
    return new_args


def usage():
    print("Usage:\n",
          "\trunlib *.so func_name [args]\n"
          "\tsupport type: {}\n".format(list(arg_types.keys())),
          "\texample:\n",
          "\t\trunlib /lib/x86_64-linux-gnu/libc.so.6 printf 'char(%s%d\\n)' 'char(9dad)' 'int(77)' --res-type=int\n"
          )


def main():
    if sys.argv.__len__() < 3:
        usage()
        sys.exit(1)
    all_args = sys.argv
    so_name, func_name = all_args[1], all_args[2]
    func_args = []
    args, res_type = parse_restype(all_args[3:])
    try:
        func_args = parse_args(args)
    except ValueError:
        usage()
        exit(1)
    func, msg = get_func(so_name, func_name)
    if func is None:
        print(msg)
        sys.exit(1)
    func.restype = getattr(ctypes, res_type)
    code = "func({})".format(', '.join(func_args))
    print('{}({})'.format(func_name, ', '.join(args)))
    ret = eval(code)
    print('res type: ', 'int' if res_type is None else res_type)
    print(ret)


if __name__ == '__main__':
    main()




