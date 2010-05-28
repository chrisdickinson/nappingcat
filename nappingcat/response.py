try:
    import json as simplejson
except ImportError:
    import simplejson

class Response(object):
    def __init__(self, status_code, content):
        self.status_code, self.content = status_code, content

    def __str__(self):
        return simplejson.dumps({"status_code":self.status_code, "content":self.content}) 

class TextResponse(Response):
    def __init__(self, status_code, content):
        super(TextResponse, self).__init__(status_code, content)

    def __str__(self):
        color = 32 if 300 > self.status_code > 199 else 31
        return "\033[0;%dm%s\033[0m\n" % (color, self.content)

def Success(content, response_type=Response):
    return response_type(200, content)
