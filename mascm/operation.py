__author__ = "Damian Giebas"
__email__ = "damian.giebas@gmail.com"
__license__ = "GNU/GPLv3"
__version__ = "0.2"

import config as c
from mascm.resource import Resource
from pycparser.c_ast import Decl, FuncCall, ID, Node, Return
import sys


class Operation:
    """Operation class"""
    def __init__(self, operation_obj: Node, thread):
        self.__operation_obj = operation_obj
        self.__thread = thread
        self.__thread.add_operation(self)
        self.__operation_number = self.__thread.num_of_operations()
        self.__name = ""
        self.__args = list()
        self.__is_last_action = False
        if isinstance(self.__operation_obj, FuncCall):
            self.__name = self.__operation_obj.name.name
            if operation_obj.args is not None:
                self.__args.extend(operation_obj.args.exprs)
        if isinstance(self.__operation_obj, Return):
            self.__is_last_action = True

    @property
    def index(self):
        """ Operation index """
        return self.__operation_number

    @property
    def name(self) -> str:
        """ Name of operation if this is function call. In other case name is empty.
        :return: String value
        """
        return self.__name

    @property
    def args(self) -> list:
        """ Function arguments list is returned
        :return: List of arguments
        """
        return self.__args

    def is_last_action(self) -> bool:
        """ If this is return operation this method return true
        :return: Boolean value
        """
        return self.__is_last_action

    def add_use_resource(self, resource: Resource) -> None:
        """ Method add resource to resource list """
        self.__args.append(resource.get_node())

    def has_func_use_the_resource(self, resource: Resource) -> bool:
        """ Method check given resource is used by operation
        :param resource: Resource object
        :return: Boolean value
        """
        for arg in self.__args:
            if isinstance(arg, ID):
                if hasattr(arg, "left") and hasattr(arg.left, "name") and resource.has_name(arg.left.name):
                    return True
                elif hasattr(arg, "name") and resource.has_name(arg.name):
                    return True
            elif isinstance(arg, Decl) and hasattr(arg, "name") and resource.has_name(arg.name):
                return True
            elif c.DEBUG:
                print(f"Cannot handle arg: {arg}", file=sys.stderr)
        return False

    def __repr__(self):
        return "o{},{}".format(str(self.__thread)[1:], self.__operation_number)

    def __lt__(self, other):
        return self.__operation_number < other.__operation_number
