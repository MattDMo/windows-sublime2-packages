import httplib

from ..console_write import console_write


class DebuggableHTTPResponse(httplib.HTTPResponse):
    """
    A custom HTTPResponse that formats debugging info for Sublime Text
    """

    _debug_protocol = 'HTTP'

    def __init__(self, sock, debuglevel=0, strict=0, method=None):
        # We have to use a positive debuglevel to get it passed to here,
        # however we don't want to use it because by default debugging prints
        # to the stdout and we can't capture it, so we use a special -1 value
        if debuglevel == 5:
            debuglevel = -1
        httplib.HTTPResponse.__init__(self, sock, debuglevel, strict, method)

    def begin(self):
        return_value = httplib.HTTPResponse.begin(self)
        if self.debuglevel == -1:
            console_write(u'Urllib2 %s Debug Read' % self._debug_protocol, True)
            headers = self.msg.headers
            versions = {
                9: 'HTTP/0.9',
                10: 'HTTP/1.0',
                11: 'HTTP/1.1'
            }
            status_line = versions[self.version] + ' ' + str(self.status) + ' ' + self.reason
            headers.insert(0, status_line)
            for line in headers:
                console_write(u"  %s" % line.rstrip())
        return return_value

    def read(self, *args):
        try:
            return httplib.HTTPResponse.read(self, *args)
        except (httplib.IncompleteRead) as (e):
            return e.partial
