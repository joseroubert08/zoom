import httplib
import json
import logging

import tornado.web

from spot.zoom.common.decorators import TimeThis


class ApplicationStateHandler(tornado.web.RequestHandler):
    @property
    def data_store(self):
        """
        :rtype: spot.zoom.www.cache.data_store.DataStore
        """
        return self.application.data_store

    @TimeThis(__file__)
    def get(self):
        try:
            logging.info('Retrieving Application State Cache')
            result = self.data_store.load_application_state_cache()
            self.write(result.to_json())

        except Exception as e:
            self.set_status(httplib.INTERNAL_SERVER_ERROR)
            self.write(json.dumps({'errorText': str(e)}))
            logging.exception(e)

        self.set_header('Content-Type', 'application/json')
