import logging
import tornado.web

from sentinel.web.handlers import LogHandler
from sentinel.web.handlers import WorkHandler


class RestServer(tornado.web.Application):
    def __init__(self, children):
        """
        :type children: dict
        """
        self.log = logging.getLogger('sent.rest')
        self.children = children
        handlers = [
            (r"/log", LogHandler),
            (r"/(?P<work>\w+)/?(?P<target>[\w|\/]+)?", WorkHandler),
        ]
        tornado.web.Application.__init__(self, handlers)
        self.log.info('Created Rest Server...')

    def get_log(self):
        """
        :rtype: list of str
        """
        logfile = 'logs/sentinel.log'
        with open(logfile, 'r') as f:
            lines = f.readlines()
            # return last 100 rows
            return [l.rstrip('\n') for l in lines[-100:]]