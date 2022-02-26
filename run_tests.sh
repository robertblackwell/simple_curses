export PYTHONPATH=./:./simple_curses:${PYTHONPATH}
python3 -m unittest tests.test_string_buffer_insert
python3 -m unittest tests.test_string_buffer_delete