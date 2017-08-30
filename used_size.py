#!/usr/bin/python
#

try:
    import gdb
except ImportError as e:
    raise ImportError("This script must be run in GDB: ", str(e))

SIZE_OF_INT = 8
SIZE_OF_BOOL = 1


def get_special_type_obj(obj_str, obj_type):
    if VectorObj.is_vector(obj_type):
        return VectorObj(obj_str, obj_type)
    if MapObj.is_map(obj_type):
        return MapObj(obj_str, obj_type)
    if CMasternodeObj.is_CMasternode(obj_type):
        return CMasternodeObj(obj_str, obj_type)
    return False


def is_special_type(type_obj):
    if not get_special_type_obj("", type_obj):
        return False
    return True


class CMasternodeObj:

    def __init__ (self, obj_name, obj_type):
        self.obj_name = obj_name
        self.obj_type = obj_type

    @classmethod
    def is_CMasternode(cls, obj_type):
        return str(obj_type) == "CMasternode"

    def get_used_size(self):
        return gdb.lookup_type("masternode_info_t").sizeof \
            + gdb.lookup_type("CMasternodePing").sizeof \
            + VectorObj.from_name(self.obj_name + ".vchSig").get_used_size() \
            + 4 * SIZE_OF_INT + 2 * SIZE_OF_BOOL \
            + MapObj.from_name(self.obj_name + ".mapGovernanceObjectsVotedOn").get_used_size()


class VectorObj:

    def __init__ (self, obj_name, obj_type):
        self.obj_name = obj_name
        self.obj_type = obj_type

    @classmethod
    def is_vector(cls, obj_type):
        type_name = str(obj_type)
        if type_name.find("std::vector<") == 0:
            return True
        return False

    @classmethod
    def from_name(cls, obj_name):
        return VectorObj(obj_name, gdb.parse_and_eval(obj_name).type)

    def element_type(self):
        return self.obj_type.template_argument(0)

    def size(self):
        return int(gdb.parse_and_eval(self.obj_name + "._M_impl._M_finish - " +
                                      self.obj_name + "._M_impl._M_start"))

    def get_used_size(self):
        if is_special_type(self.element_type()):
            size = 0
            for i in range(self.size()):
                elem_str = "(" + self.obj_name + "._M_impl._M_start + " + str(i) + ")"
                obj = get_special_type_obj(elem_str, self.element_type())
                size += obj.get_used_size()
            return size
        return self.size() * self.element_type().sizeof


class MapObj:

    def __init__ (self, obj_name, obj_type):
        self.obj_name = obj_name
        self.obj_type = obj_type

    @classmethod
    def is_map(cls, obj_type):
        type_name = str(obj_type)
        if type_name.find("std::map<") == 0:
            return True
        return False

    @classmethod
    def from_name(cls, obj_name):
        return MapObj(obj_name, gdb.parse_and_eval(obj_name).type)

    def key_type(self):
        return self.obj_type.template_argument(0)

    def value_type(self):
        return self.obj_type.template_argument(1)

    def size(self):
        return int(gdb.parse_and_eval(self.obj_name + "._M_t->_M_impl->_M_node_count"))

    def get_used_size(self):
        if not is_special_type(self.key_type()) and not is_special_type(self.value_type()):
            return self.size() * (self.key_type().sizeof + self.value_type().sizeof)
        if self.size() == 0:
            return self.obj_type.sizeof
        size = 0
        gdb.execute("set $status = 1")
        gdb.execute("p $status")
        print ("set $node = " + self.obj_name + "->_M_t->_M_impl->_M_header->_M_left")
        gdb.execute("p " + self.obj_name)
        gdb.execute("set $node = " + self.obj_name + "->_M_t->_M_impl->_M_header->_M_left")
        gdb.execute("set $status = 2")
        gdb.execute("p $status")
        for i in range(self.size()):
            gdb.execute("set $status = 3")
            gdb.execute("p $status")
            gdb.execute("set $value = (void*)($node + 1)")
            gdb.execute("set $status = 4")
            gdb.execute("p $status")
            if is_special_type(self.key_type()):
                gdb.execute("set $status = 5")
                gdb.execute("p $status")
                key_elem_str = "*(" + str(self.key_type()) + "*)$value"
                obj = get_special_type_obj(key_elem_str, self.key_type())
                gdb.execute("set $status = 6")
                gdb.execute("p $status")
                size += obj.get_used_size()
                gdb.execute("set $status = 7")
                gdb.execute("p $status")
            else:
                gdb.execute("set $status = 8")
                gdb.execute("p $status")
                size += gdb.key_type().sizeof
                gdb.execute("set $status = 9")
                gdb.execute("p $status")

            gdb.execute("set $status = 10")
            gdb.execute("p $status")
            gdb.execute("set $value = $value + 4")
            gdb.execute("set $status = 11")
            gdb.execute("p $status")
            if is_special_type(self.value_type()):
                gdb.execute("set $status = 12")
                gdb.execute("p $status")
                value_elem_str = "*(" + str(self.value_type()) + "*)$value"
                obj = get_special_type_obj(value_elem_str, self.value_type())
                gdb.execute("set $status = 13")
                gdb.execute("p $status")
                size += obj.get_used_size()
                gdb.execute("set $status = 14")
                gdb.execute("p $status")
            else:
                gdb.execute("set $status = 15")
                gdb.execute("p $status")
                size += gdb.key_type().sizeof
                gdb.execute("set $status = 16")
                gdb.execute("p $status")

            gdb.execute("set $status = 17")
            gdb.execute("p $status")
            if gdb.parse_and_eval("$node->_M_right") != 0:
                gdb.execute("set $status = 18")
                gdb.execute("p $status")
                gdb.execute("set $node = $node->_M_right")
                gdb.execute("set $status = 19")
                gdb.execute("p $status")
                while gdb.parse_and_eval("$node->_M_left") != 0:
                    gdb.execute("set $status = 20")
                    gdb.execute("p $status")
                    gdb.execute("set $node = $node->_M_left")
                    gdb.execute("set $status = 21")
                    gdb.execute("p $status")
            else:
                gdb.execute("set $status = 22")
                gdb.execute("p $status")
                gdb.execute("set $tmp_node = $node->_M_parent")
                gdb.execute("set $status = 23")
                gdb.execute("p $status")
                while gdb.parse_and_eval("$node") == gdb.parse_and_eval("$tmp_node->_M_right"):
                    gdb.execute("set $status = 24")
                    gdb.execute("p $status")
                    gdb.execute("set $node = $tmp_node")
                    gdb.execute("set $status = 25")
                    gdb.execute("p $status")
                    gdb.execute("set $tmp_node = $tmp_node->_M_parent")
                    gdb.execute("set $status = 26")
                    gdb.execute("p $status")
                gdb.execute("set $status = 27")
                gdb.execute("p $status")
                if gdb.parse_and_eval("$node->_M_right") != gdb.parse_and_eval("$tmp_node"):
                    gdb.execute("set $status = 28")
                    gdb.execute("p $status")
                    gdb.execute("set $node = $tmp_node")
                    gdb.execute("set $status = 29")
                    gdb.execute("p $status")
        return size


class UsedSizeCommand (gdb.Command):
    """calc size of the memory used by the object"""

    def __init__ (self):
        super (UsedSizeCommand, self).__init__ ("usedsize", gdb.COMMAND_USER)

    def assign_value(self, obj_name, value):
        gdb.execute("set " + obj_name + " = " + str(value))

    def get_type(self, obj_name):
        return gdb.parse_and_eval(obj_name).type

    def invoke (self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        obj_type = self.get_type(args[1])
        print (args[1] + " is " + str(obj_type))
        obj = get_special_type_obj(args[1], obj_type)
        if not obj:
            size = obj_type.sizeof
        else:
            size = obj.get_used_size()
        self.assign_value(args[0], size)
        size_obj = gdb.parse_and_eval(args[0])
        print (size_obj)

UsedSizeCommand()
