import sys
import os
from imp import reload

dirname = os.path.split(os.path.dirname(__file__))[1]


all_modules = ["command", "data_struct", "utils"]


def reload_module():
    for module in all_modules:
        name = "%s.%s" % (dirname, module)
        reload(sys.modules[name])


def plugin_loaded():
    reload_module()


def plugin_unloaded():
    pass
