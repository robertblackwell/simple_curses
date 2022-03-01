import curses
import curses.textpad


class Colors:
    _instance = None
    def __init__(self):
        raise RuntimeError('Call instance() instead')
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.COLOR_RED_BLACK = 1
            cls._instance.COLOR_CYAN_BLACK = 2
            cls._instance.COLOR_GREEN_BLACK = 3
            cls._instance.COLOR_BLACK_YELLOW = 4
            cls._instance.COLOR_BLUE_WHITE = 5
            cls._instance.COLOR_BLACK_WHITE = 6
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_YELLOW)
            curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
            curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
        else:
            pass
        return cls._instance
    
    def get(self, pair_nbr):
        tmp = curses.color_pair(pair_nbr)
        return tmp

    
    def msg_info(self):
        pass

    @classmethod
    def button_focus(cls):
        return curses.color_pair(cls.instance().COLOR_BLACK_YELLOW) + curses.A_BOLD
    
    @classmethod
    def button_no_focus(cls):
        return curses.color_pair(cls.instance().COLOR_BLUE_WHITE) + curses.A_BOLD

    @classmethod
    def msg_label_attr(cls):
        c: Colors = cls.instance()
        return curses.color_pair(c.COLOR_GREEN_BLACK) +  curses.A_BOLD

    @classmethod
    def msg_error_attr(cls):
        c: Colors = cls.instance()
        return curses.color_pair(c.COLOR_RED_BLACK) +  curses.A_BLINK
    
    @classmethod
    def title_attr(cls):
        c: Colors = cls.instance()
        return curses.color_pair(c.COLOR_BLACK_WHITE) +  curses.A_BOLD

def kolors():
    return Colors.instance()


