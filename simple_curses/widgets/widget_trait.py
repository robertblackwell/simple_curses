from simple_curses.widget_base import WidgetBase

class WidgetTrait(WidgetBase):
    def get_height(self):
        return self.height
    def get_width(self):
        return self.width