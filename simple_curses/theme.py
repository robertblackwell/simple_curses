"""
The functions in this file implement a theme for simple_cursers apps
"""
import curses
from simple_curses.colors import Colors



class WhiteBackground:
    def __init__(self):
        self._bkgd_attr = Colors.black_white()
        self._bkgd_attr = Colors.black_white()
        self._cursor_attr = Colors.white_black() + curses.A_REVERSE
        self._label_focus_attr = Colors.blue_white()
        self._label_nofocus_attr = Colors.black_white()
        self._value_focus_attr = Colors.white_black()
        self._value_nofocus_attr = Colors.black_white()
        c: Colors = Colors.instance()
        self._msg_label_attr = curses.color_pair(c.COLOR_GREEN_BLACK) + curses.A_BOLD
        self._msg_error_attr = curses.color_pair(c.COLOR_RED_BLACK) + curses.A_BOLD
        self._msg_warn_attr = curses.color_pair(c.COLOR_YELLOW_BLACK) + curses.A_BOLD
        self._msg_info_attr = curses.color_pair(c.COLOR_GREEN_BLACK) + curses.A_BOLD

class BlackBackground:
    def __init__(self):
        self._bkgd_attr = Colors.white_black()
        self._cursor_attr = Colors.yellow_black() + curses.A_REVERSE #+ curses.A_STANDOUT
        self._label_focus_attr = Colors.green_black()
        self._label_nofocus_attr = Colors.white_black()
        self._value_focus_attr = Colors.green_black()
        self._value_nofocus_attr = Colors.white_black()
        c: Colors = Colors.instance()
        self._msg_label_attr = curses.color_pair(c.COLOR_GREEN_BLACK) + curses.A_BOLD
        self._msg_error_attr = curses.color_pair(c.COLOR_RED_BLACK) + curses.A_BOLD
        self._msg_warn_attr = curses.color_pair(c.COLOR_YELLOW_BLACK) + curses.A_BOLD
        self._msg_info_attr = curses.color_pair(c.COLOR_GREEN_BLACK) + curses.A_BOLD

class Theme():
    _instance = None

    def __init__(self):
        self.attributes = None
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.attributes = BlackBackground()
        else:
            pass
        return cls._instance

    def bkgd_attr(self):
        return self.attributes._bkgd_attr

    def cursor_attr(self):
        return self.attributes._cursor_attr

    def label_attr(self, with_focus: bool):
        if with_focus:
            return self.attributes._label_focus_attr
        else:
            return self.attributes._label_nofocus_attr

    def value_attr(self, with_focus: bool):
        if with_focus:
            return self.attributes._value_focus_attr
        else:
            return self.attributes._value_nofocus_attr

    def msg_attr(self):
        return self.attributes._msg_attr

    def msg_label_attr(self):
        return self.attributes._msg_label_attr

    def msg_error_attr(self):
        return self.attributes._msg_error_attr

    def msg_warn_attr(self):
        return self.attributes._msg_warn_attr

    def msg_info_attr(self):
        return self.attributes._msg_info_attr

