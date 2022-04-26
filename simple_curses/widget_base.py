from abc import ABC, abstractmethod, abstractproperty
import curses
import curses.textpad
from typing import Any

from simple_curses.theme import Theme
from simple_curses.keyboard import *
from simple_curses.kurses_ex import *


class WidgetBase(ABC):
    """
    An interface describing the minimum required methods for any class that represents
    something that can be displayed in part of a simple_curses application screen. 
    
    The basic widget only provides for display and includes no user interaction
    """

    # @classmethod
    @abstractmethod
    def get_height(self) -> int:
        """Returns the minimum height required to display the widget"""
        raise NotImplementedError()

    @abstractmethod
    def get_width(self) -> int:
        """Returns the minimum width required to display the widget"""
        raise NotImplementedError()

    @abstractmethod
    def render(self) -> None:
        """Draws the widget on the screen using curses functions"""
        raise NotImplementedError()

    @abstractmethod
    def handle_input(self, ch) -> bool:
        """
        Handles the input character in whatever manner is appropriate for this widget.

        Return Rrue if the ch was consumed and it should not be passed to other char handlers
        Return False is the ch was not of interest to this widget
        
        """
        raise NotImplementedError()

    @abstractmethod
    def set_enclosing_window(self, win) -> None:
        """Each widget is displayed inside a curses.window and requires a curses.window in order to 
        perform output of character data.
        In addition the win parameter provides the size and location of the rectable on the screen
        where the widget should be displayed
        Widgets are free to create additional curses.windows as subwins of win if that is 
        a convenient of managing the display process
        """
        raise NotImplementedError()

    def set_parent_view(self, view):
        self.parent_view = view


class FocusableWidgetBase(WidgetBase):
    """A widget that can accept the focus. Typically the display of the
    widget will change to give indication to a user that this widget
    now has the focus.
    
    Having the focus is a necessary condition for editing/updating the content of widgets
    that contain values
    
    Focusable widgets do not contain values
    """

    @abstractmethod
    def focus_accept(self) -> None:
        """This function is called by a 'higher' object to indicate that the focus is being passed to
        this widget. the widget shold probably remember this fact if it is required to 
        display the fact that it has the focus"""
        raise NotImplementedError()

    @abstractmethod
    def focus_release(self) -> None:
        """called by a 'higher' object to indicate that the focus is moving away from this widget"""
        raise NotImplementedError()


class EditableWidgetBase(FocusableWidgetBase):
    """A widget that contains a key or id and a value"""

    @abstractmethod
    
    def get_key(self) -> str:
        """Returns the key or id string assigned during instance creation.
        The key is used outside the widget to associate the widgets value with
        a program variable"""
        raise NotImplementedError()

    @abstractmethod
    def get_value(self):
        """Return the value (usually a string but not always) held inside this widget.
        """
        raise NotImplementedError()

    @abstractmethod
    def set_value(self, v):
        """Sets the value held inside this widget. This value MUST be set to something compatible with
        the widget before any attempt to display the widget"""
        raise NotImplementedError()

    @abstractmethod
    def clear(self) -> None:
        """Deprecated"""
        raise NotImplementedError()


class MenuBase(FocusableWidgetBase):
    """A menu item is a widget that can accept the focus, cannot be edited(ie does not contain a value), 
    but can be 'invoked' to call an action function
    In simple_curses applications there is a distinction between how menu items and other widgets are
    given the focus.


    Menu items receive focus by the user hitting the function key that is associated with the menu item,
    where as for other widgets the focus is passed around by TAB/SHIFT-TAB
    """

    @abstractmethod
    def get_accelerator(self):
        """Returns the integer value provided by curses for the function key that has been
        associated with this menu item.
        Hitting a menu items accelerator key will have the effect of:
        -   giving the focus to that menu item
        -   invoking the menu items action function"""
        raise NotImplementedError()

    @abstractmethod
    def invoke(self):
        """This is how the menus action is triggered. Typically it calls a function that was passed
        to a menu item constructor at instance creation"""
        raise NotImplementedError()


def is_widget(w):
    """Returns true if w is derived from WidgetBase False otherwise"""
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
    """Returns True if w is derived from Focusable False otherwise"""
    x0 = isinstance(widget, FocusableWidgetBase) or isinstance(widget, EditableWidgetBase)
    return x0
    x0 = hasattr(widget, "focus_accept") and callable(getattr(widget, "focus_accept"))
    x1 = hasattr(widget, "focus_relase") and callable(getattr(widget, "focus_release"))
    return hasattr(widget, "focus_accept") and callable(getattr(widget, "focus_accept")) and hasattr(widget,
                                                                                                     "focus_relase") and callable(
        getattr(widget, "focus_release"))


def is_editable(widget):
    """Returns True if w is derived from Editable False otherwise"""
    x0 = isinstance(widget, EditableWidgetBase)
    return x0
    x0 = is_focusable(widget)
    x1 = hasattr(widget, "get_value") and callable(getattr(widget, "get_value"))
    x2 = hasattr(widget, "clear") and callable(getattr(widget, "clear"))
    res = is_focusable(widget) and hasattr(widget, "get_value") and callable(getattr(widget, "get_value")) and hasattr(
        widget, "clear") and callable(getattr(widget, "clear"))
    return res
