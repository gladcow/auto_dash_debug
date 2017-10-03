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


class LogDetailedCommand (gdb.Command):
    """write detailed info about the object to the file"""

    def __init__ (self):
        super (LogDetailedCommand, self).__init__ ("logdetailed", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        try:
            args = gdb.string_to_argv(arg)
            obj = args[0]
            obj_type = gdb.parse_and_eval(obj).type
            logfile = open(args[1], 'a')
            size = common_helpers.get_instance_size(obj, obj_type)
            logfile.write("%s %s: %d\n" % (str(datetime.datetime.now()), str(obj), size))
            logfile.close()
        except gdb.error as e:
            print(traceback.format_exc())
            raise e

LogDetailedCommand()
