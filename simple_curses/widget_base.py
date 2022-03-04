
from abc import ABC, abstractmethod, abstractproperty
import curses
import curses.textpad

from form import Form


class WidgetBase(ABC):
    @classmethod
    @abstractmethod
    def classmeth(cls):
        pass

    @abstractmethod
    def foobar(self):
        pass

    @abstractmethod
    def get_height(self) -> int:
        pass
    @abstractmethod
    def get_width(self) -> int:
        pass
    @abstractmethod
    def focus_accept(self) -> None:
        pass
    @abstractmethod
    def focus_release(self) -> None:
        pass
    @abstractmethod
    def render(self) -> None:
        pass
    @abstractmethod
    def handle_input(self, ch) -> bool:
        pass
    @abstractmethod
    def set_enclosing_window(self, win: curses.window) -> None:
        pass
    @abstractmethod
    def set_form(self, form: Form) -> None:
        pass

class MenuBase(WidgetBase):

    @abstractmethod
    def invoke(self):
        pass