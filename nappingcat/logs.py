import sys

# TODO make configurable
COLOR_BAD = 31
COLOR_GOOD = 32

class ColorLogger(object):
    def __init__(self, to_stream):
        self.stream = to_stream

    def good(self, what):
        self.output(COLOR_GOOD, what)

    def bad(self, what):
        self.output(COLOR_BAD, what)

    def output(self, color, what):
        output = "\033[0;%dm%s\033[0m" % (color, what)
        self.stream.write(output)
        self.stream.flush()
        
