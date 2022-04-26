from abc import ABC, abstractmethod, abstractproperty
import curses
import curses.textpad
from typing import Any

from simple_curses.theme import Theme
from simple_curses.keyboard import *
from simple_curses.kurses_ex import *


class WidgetBase(ABC):
    """A basic widget that can display fixed text on the screen"""

    # @classmethod
    @abstractmethod
    def get_height(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_width(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def handle_input(self, ch) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def set_enclosing_window(self, win) -> None:
        raise NotImplementedError()

    def set_parent_view(self, view):
        self.parent_view = view

    def get_key(self) -> str:
        raise NotImplementedError()


class FocusableWidgetBase(WidgetBase):
    """A widget that can accept the focus and may be able to navigate around its fixed text display"""

    @abstractmethod
    def focus_accept(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def focus_release(self) -> None:
        raise NotImplementedError()


class EditableWidgetBase(FocusableWidgetBase):
    """A widget that contains one of more variable fields that can be edited by the user"""

    @abstractmethod
    def get_value(self):
        raise NotImplementedError()

    @abstractmethod
    def set_value(self, v):
        raise NotImplementedError()

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError()


class MenuBase(FocusableWidgetBase):
    "A widget that can accept the focus, cannot be edited, but can be 'invoked' to call an action function"

    @abstractmethod
    def invoke(self):
        raise NotImplementedError()


def is_widget(w):
    x0 = isinstance(w, WidgetBase)
    return x0
    return hasattr(w, "get_height") \
           and callable(getattr(w, "get_height")) \
           and hasattr(w, "get_width") \
           and callable(getattr(w, "get_width")) \
           and hasattr(w, "get_width") \
           and callable(getattr(w, "render")) \
           and hasattr(w, "render") \
           and callable(getattr(w, "set_enclosing_window")) \
           and hasattr(w, "handle_input") \
           and callable(getattr(w, "handle_input"))


def is_focusable(widget):
    x0 = isinstance(widget, FocusableWidgetBase) or isinstance(widget, EditableWidgetBase)
    return x0
    x0 = hasattr(widget, "focus_accept") and callable(getattr(widget, "focus_accept"))
    x1 = hasattr(widget, "focus_relase") and callable(getattr(widget, "focus_release"))
    return hasattr(widget, "focus_accept") and callable(getattr(widget, "focus_accept")) and hasattr(widget,
                                                                                                     "focus_relase") and callable(
        getattr(widget, "focus_release"))


def is_editable(widget):
    x0 = isinstance(widget, EditableWidgetBase)
    return x0
    x0 = is_focusable(widget)
    x1 = hasattr(widget, "get_value") and callable(getattr(widget, "get_value"))
    x2 = hasattr(widget, "clear") and callable(getattr(widget, "clear"))
    res = is_focusable(widget) and hasattr(widget, "get_value") and callable(getattr(widget, "get_value")) and hasattr(
        widget, "clear") and callable(getattr(widget, "clear"))
    return res
