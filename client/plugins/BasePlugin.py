from PyQt5.QtWidgets import QPlainTextEdit


class BasePlugin:
    """
    Base plugin class for fastnote plugins.
    Realise this class in new file in folder plugins with class called "Plugin"

    Static attributes that you may change:
    NAME - NAME OF YOUR PLUGIN THAT SHOWS IN EDITOR
    SHORTCUT - SHORTCUT FOR FUNCTION "on_call". MAY BE NONE
    AUTHOR - AUTHOR CREDITS

    Realise plugin logic at on_init() and on_call() methods
    """

    NAME = "BasePlugin"  # NAME OF YOUR PLUGIN THAT SHOWS IN EDITOR
    SHORTCUT = None  # SHORTCUT FOR FUNCTION "on_call". MAY BE NONE
    AUTHOR = "Rodion Sarygin"  # AUTHOR CREDITS
    DESCRIPTION = "BasePluginDescription"  # DESCRIPTION FOR PLUGIN

    @classmethod
    def on_init(cls, parent=None):
        """Runned once when plugin is loaded"""
        pass

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit, parent=None):
        """Runned every time when user clicking button for plugin"""
        pass
