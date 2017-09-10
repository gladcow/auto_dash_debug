#!/usr/bin/python
#

try:
    import gdb
except ImportError as e:
    raise ImportError("This script must be run in GDB: ", str(e))
import sys
import os
sys.path.append(os.getcwd())
import common_helpers
import stl_containers


class CDarksendQueueObj:

    def __init__ (self, obj_name, obj_type):
        self.obj_name = obj_name
        self.obj_type = obj_type

    @classmethod
    def is_this_type(cls, obj_type):
        return str(obj_type) == "CDarksendQueue"

    def get_used_size(self):
        return common_helpers.SIZE_OF_INT \
            + common_helpers.get_instance_size("(" + self.obj_name + ").vin", gdb.lookup_type("CTxIn")) \
            + common_helpers.SIZE_OF_INT64 + common_helpers.SIZE_OF_BOOL \
            + stl_containers.VectorObj.from_name("(" + self.obj_name + ").vchSig").get_used_size() \
            + common_helpers.SIZE_OF_BOOL


class CDarkSendEntryObj:

    def __init__ (self, obj_name, obj_type):
        self.obj_name = obj_name
        self.obj_type = obj_type

    @classmethod
    def is_this_type(cls, obj_type):
        return str(obj_type) == "CDarkSendEntry"

    def get_used_size(self):
        return stl_containers.VectorObj.from_name("(" + self.obj_name + ").vecTxDSIn").get_used_size() \
            + stl_containers.VectorObj.from_name("(" + self.obj_name + ").vecTxDSOut").get_used_size() \
            + common_helpers.get_instance_size("(" + self.obj_name + ").txCollateral", gdb.lookup_type("CTransaction")) \
            + common_helpers.get_instance_size("(" + self.obj_name + ").addr", gdb.lookup_type("CService"))

