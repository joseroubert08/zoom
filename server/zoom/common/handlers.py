import logging
from tornado.web import RequestHandler


class LogVerbosityHandler(RequestHandler):
    def post(self, level):
        """
        @api {get} /loglevel/:level Set logging level for log file
        @apiDescription Available parameters are debug, info, and warning.
        Everything else will be dropped.
        @apiVersion 1.0.0
        @apiName SetLogLevel
        @apiGroup Common
        """
        logger = logging.getLogger('')
        level = level.lower()
        if level == 'debug':
            logger.setLevel(logging.DEBUG)
        elif level == 'info':
            logger.setLevel(logging.INFO)
        elif level == 'warning':
            logger.setLevel(logging.WARNING)
        else:
            return

        msg = 'Changed log level to {0}'.format(level)
        logging.info(msg)
        self.write(msg)


class RUOKHandler(RequestHandler):
    def get(self):
        """
        @api {get} /ruok Return whether the web server is available
        @apiDescription This is currently only used by the init script so that it
        will block until the web server is available.
        @apiVersion 1.0.0
        @apiName WebAvailable
        @apiGroup Common
        """
        self.write('ok')

class VersionHandler(RequestHandler):
    def get(self):
        """
        @api {get} /version Return the version of the software
        @apiDescription Return the running version of the software
        @apiVersion 1.0.0
        @apiName Version
        @apiGroup Common
        """
        self.write(self.application.version)
