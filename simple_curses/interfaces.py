from typing import Any, List, Dict
from abc import ABC, abstractmethod

class Sizeable:
    @abstractmethod
    def get_height(self):
        raise NotImplementedError()
    
    @abstractmethod
    def get_width(self):
        raise NotImplementedError()

    def get_size(self):
        return (self.get_height(), self.get_width())

class Renderable(Sizeable):
    @abstractmethod
    def set_enclosing_window(curses_win):
        raise NotImplementedError()
    @abstractmethod
    def render(self):
        raise NotImplementedError()

class Focusable(Renderable):
    @abstractmethod
    def focus_accept(self):
        raise NotImplementedError()

    @abstractmethod
    def focus_release(self):
        raise NotImplementedError()

    @abstractmethod
    def handle_input(self, key_code):
        raise NotImplementedError()

class Editable(Focusable):
    @abstractmethod
    def get_key(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_value(self) -> Any:
        raise NotImplementedError()

    def set_value(self, value: Any) -> None:
        raise NotImplementedError()

class View(Focusable):
    @abstractmethod
    def get_keys(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_values(self) -> Dict[str, Any]: 
        raise NotImplementedError()

    @abstractmethod
    def set_value(self, values: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def show(self):
        raise NotImplementedError()

    @abstractmethod
    def hide(self):
        raise NotImplementedError()


