import sys

# TODO make configurable
COLOR_BAD = 31
COLOR_GOOD = 32

class ColorLogger(object):
    def good(self, what, to_stream=sys.stderr):
        self.output(COLOR_GOOD, what, to_stream=to_stream)

    def bad(self, what, to_stream=sys.stderr):
        self.output(COLOR_BAD, what, to_stream=to_stream)

    def output(self, color, what, to_stream=sys.stderr):
        output = "\033[0;%dm%s\033[0m" % (color, what)
        print >>to_stream, output

