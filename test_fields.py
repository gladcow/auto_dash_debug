#!/usr/bin/python
#

try:
    import gdb
except ImportError as e:
    raise ImportError("This script must be run in GDB: ", str(e))
import traceback



class TestFieldsCommand (gdb.Command):
    """explore fields"""

    def __init__ (self):
        super (TestFieldsCommand, self).__init__ ("testfields", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        try:
            args = gdb.string_to_argv(arg)
            obj = args[0]
            obj_type = gdb.parse_and_eval(obj).type
            fields = obj_type.fields()
            for f in fields:
                print("*****************")
                print(hasattr(f, "bitpos"))
                print("Field %s has type %s" % (f.name, str(f.type)))
        except gdb.error as e:
            print(traceback.format_exc())
            raise e

TestFieldsCommand()
