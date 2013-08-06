import urllib2

from .debuggable_http_connection import DebuggableHTTPConnection


class DebuggableHTTPHandler(urllib2.HTTPHandler):
    """
    A custom HTTPHandler that formats debugging info for Sublime Text
    """

    def __init__(self, debuglevel=0, debug=False, **kwargs):
        # This is a special value that will not trigger the standard debug
        # functionality, but custom code where we can format the output
        if debug:
            self._debuglevel = 5
        else:
            self._debuglevel = debuglevel
        self.passwd = kwargs.get('passwd')

    def http_open(self, req):
        def http_class_wrapper(host, **kwargs):
            kwargs['passwd'] = self.passwd
            return DebuggableHTTPConnection(host, **kwargs)

        return self.do_open(http_class_wrapper, req)
