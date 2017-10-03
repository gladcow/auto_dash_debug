#!/usr/bin/python
#

try:
    import gdb
except ImportError as e:
    raise ImportError("This script must be run in GDB: ", str(e))
import traceback
import datetime
import sys
import os
sys.path.append(os.getcwd())
import common_helpers
import cProfile


class LogSizeCommand (gdb.Command):
    """calc size of the memory used by the object and write it to file"""

    def __init__ (self):
        super (LogSizeCommand, self).__init__ ("logsize", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        try:
            args = gdb.string_to_argv(arg)
            obj = args[0]
            obj_type = gdb.parse_and_eval(obj).type
            logfile = open(args[1], 'a')
            profile = cProfile.Profile()
            profile.enable()
            size = common_helpers.get_instance_size(obj, obj_type)
            profile.disable()
            profile.dump_stats('py_profile.txt')
            logfile.write("%s %s: %d\n" % (str(datetime.datetime.now()), str(obj), size))
            logfile.close()
        except gdb.error as e:
            print(traceback.format_exc())
            raise e

LogSizeCommand()
