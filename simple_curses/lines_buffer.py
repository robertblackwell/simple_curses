class LinesBuffer:
    def __init__(self, lines, capacity, view_height):
        self.lines = []
        self.capacity = capacity
        self.view_height = view_height
        self.cpos_lines = 0
        self.cpos_view = 0
        self.first_line = 0
        self.last_line = 0
        for line in lines:
            self.append_line(line)


    def _incr_cpos_lines(self):
        self.cpos_lines = self.cpos_lines + 1 if self.cpos_lines < len(self.lines) - 1 else len(self.lines) - 1 

    def _decr_cpos_lines(self):
        self.cpos_lines = self.cpos_lines - 1 if self.cpos_lines > 0 else 0 

    def _incr_cpos_view(self):
        self.cpos_view = self.cpos_view + 1 if self.cpos_view < self.view_height - 1 else self.view_height - 1 

    def _decr_cpos_view(self):
        self.cpos_view = self.cpos_view - 1 if self.cpos_view > 0 else 0 

    def _compute_view(self):
        self.first_line = self.cpos_lines - self.cpos_view
        self.last_line = self.first_line + self.view_height

    def handle_up(self):
        self._decr_cpos_lines()
        self._decr_cpos_view()
        self._compute_view()

    def handle_down(self):
        self._incr_cpos_lines()
        self._incr_cpos_view()
        self._compute_view()

    def append_line(self, line):
        if len(self.lines) == 0:
            self.lines.append(line)
        else:
            self.lines.append(line)
            self._incr_cpos_lines()
            self._incr_cpos_view()
        self._compute_view()

    def handle_add_line(self, line):
        pass
    def handle_delete_line(self):
        pass

    def get_view(self):
        result = []
        for i in range(self.first_line, self.last_line):
            result.append((i, self.lines[i]))
        return result

    def print_view(self):
        view = self.get_view()
        for line in view:
            print("{0:>6}| {1}".format(line[0], line[1]))