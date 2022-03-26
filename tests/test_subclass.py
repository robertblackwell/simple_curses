import unittest
from  simple_curses import FocusableWidgetBase, MenuBase, is_focusable, DummyMenuItem, MenuItem

class Fred(MenuBase):
    pass

class Jim(MenuItem):
    def __init__(self):
        super().__init__(None, "alabel", 12, 12, "", None, None)

class TestSubclass(unittest.TestCase):

    def test_integer(self):
        widget = MenuItem(None, "alabel", 12, 12, "", None, None)
        x = is_focusable(widget)
        y = issubclass(widget.__class__, FocusableWidgetBase)
        z = isinstance(widget, FocusableWidgetBase)
        widget = DummyMenuItem(None, "alabel", 12, 12, "", None, None)
        x = is_focusable(widget)
        y = issubclass(widget.__class__, FocusableWidgetBase)
        z = isinstance(widget, FocusableWidgetBase)
        w2 = Fred()
        x = is_focusable(w2)
        y = issubclass(w2.__class__, FocusableWidgetBase)
        z = isinstance(w2, FocusableWidgetBase)
        w2 = Jim()
        x = is_focusable(w2)
        y = issubclass(w2.__class__, FocusableWidgetBase)
        z = isinstance(w2, FocusableWidgetBase)
        print("Hello")
if __name__ == '__main__':
    unittest.main()
