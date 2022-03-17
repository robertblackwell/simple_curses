from abc import ABC, abstractmethod, abstractproperty
import curses
import curses.textpad


class WidgetBase(ABC):
    """A basic widget that can display fixed text on the screen"""

    @classmethod
    @abstractmethod
    def classmeth(cls):
        pass

    # @abstractmethod
    # def foobar(self):
    #     pass

    @abstractmethod
    def get_height(self) -> int:
        pass

    @abstractmethod
    def get_width(self) -> int:
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
    def set_form(self, form) -> None:
        pass


class FocusableWidgetBase(WidgetBase):
    """A widget that can accept the focus and may be able to navigate around its fixed text display"""

    @abstractmethod
    def focus_accept(self) -> None:
        pass

    @abstractmethod
    def focus_release(self) -> None:
        pass


class EditableWidgetBase(FocusableWidgetBase):
    """A widget that contains one of more variable fields that can be edited by the user"""

    @abstractmethod
    def get_value(self) -> str:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass


class MenuBase(FocusableWidgetBase):
    "A widget that can accept the focus, cannot be edited, but can be 'invoked' to call an action function"

    @abstractmethod
    def invoke(self):
        pass
