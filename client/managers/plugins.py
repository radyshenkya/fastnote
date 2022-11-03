from os import path
from util.debug import debug
from util.files import list_dirs_in_dir, load_module_from_file


class PluginManager:
    def __init__(self, plugin_modules) -> None:
        self.plugins = []

        for mod in plugin_modules:
            try:
                self.plugins.append(mod.Plugin)
            except Exception as e:
                debug("Could not load plugin", mod.__file__)
                debug("Exception:", e)

    def init_plugins(self, parent=None):
        for plugin in self.plugins:
            try:
                plugin.on_init(parent)
            except Exception as e:
                debug("Exception on initializing plugin", plugin.NAME)
                debug("Exception:", e)

    @staticmethod
    def load_from_folder(folder_path: str) -> "PluginManager":
        debug("Loading plugins from", folder_path)

        # listing all directories in plugins folder
        dirs = [path.join(folder_path, el) for el in list_dirs_in_dir(
            folder_path) if el != "__pycache__"]

        # loading modules
        modules = []
        for dir in dirs:
            try:
                module = load_module_from_file(
                    "plugin", path.join(dir, "plugin.py"))
                modules.append(module)
            except Exception as e:
                debug("Can not load plugin.py module at", dir)
                debug("Exception:", e)

        return PluginManager(modules)
