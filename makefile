all: test

test: test_string_buffer

test_string_buffer:
	python3 -m unittest discover -k TestStringBuffer tests