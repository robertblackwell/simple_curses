import unittest
from  simple_curses import FocusableWidgetBase, \
        EditableWidgetBase, WidgetBase, MenuBase, \
        is_focusable, DummyMenuItem, MenuItem, \
        TextWidget, MultiLineWidget, DummyMultiLineWidget, IntegerWidget, ToggleWidget, TitleWidget, \
            BlockTextWidget
from widget_base import is_editable, is_widget

class Fred(MenuBase):
    pass

class Jim(MenuItem):
    def __init__(self):
        super().__init__(None, "alabel", 12, 12, "", None, None)

class TestSubclass(unittest.TestCase):

    def test_multiline(self):
        widget = MultiLineWidget(None, "one", "MUltiline", 30, 20, "") 
        # zz = widget.__class__.__mro__
        # zz_d = widget_d.__class__.__mro__
        # print(zz)
        # print(zz_d)
        self.assertTrue(is_focusable(widget))
        self.assertTrue(is_editable(widget))
        self.assertTrue(is_widget(widget))
        print("Hello")

    def test_integerwidget(self):
        widget = IntegerWidget(None, "one", "TextWidget", 30, "") 
        self.assertTrue(is_focusable(widget))
        self.assertTrue(is_editable(widget))
        self.assertTrue(is_widget(widget))
        print("Hello")

    def test_textwidget(self):
        widget = TextWidget(None, "one", "TextWidget", 30, "") 
        self.assertTrue(is_focusable(widget))
        self.assertTrue(is_editable(widget))
        self.assertTrue(is_widget(widget))
        print("Hello")

    def test_togglewidget(self):
        widget = ToggleWidget(None, "one", "TextWidget", 30, "", ["One", "Two"]) 
        self.assertTrue(is_focusable(widget))
        self.assertTrue(is_editable(widget))
        self.assertTrue(is_widget(widget))
        print("Hello")

    def test_titlewidget(self):
        widget = TitleWidget(None, "one", "TextWidget", 30, 20, "") 
        self.assertTrue(not is_focusable(widget))
        self.assertTrue(not is_editable(widget))
        self.assertTrue(is_widget(widget))
        print("Hello")

    def test_blocktextwidget(self):
        widget = BlockTextWidget(None, ["one", "TextWidget"]) 
        self.assertTrue(not is_focusable(widget))
        self.assertTrue(not is_editable(widget))
        self.assertTrue(is_widget(widget))
        print("Hello")


    def test_menuitem(self):
        widget = MenuItem(None, "alabel", 12, 12, "", None, None)
        self.assertTrue(is_focusable(widget))
        self.assertTrue(not is_editable(widget))
        self.assertTrue(is_widget(widget))

if __name__ == '__main__':
    unittest.main()
