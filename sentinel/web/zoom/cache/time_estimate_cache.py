import httplib
import json
import logging
import requests
import tornado.web
from zoom.entities.types import DependencyType


class TimeEstimateCache(object):

    def __init__(self, configuration, application_state_cache, application_dependency_cache):

        self.dep_cache = application_dependency_cache
        self.state_cache = application_state_cache
        self.graphite_cache = {}
        self.configuration = configuration

    def reload(self):
        self.graphite_cache.clear()

    def load(self):
        logging.info("Loading Timing Estimates...")
        try:
            self.deps = self.dep_cache.load().application_dependencies
            self.states = self.state_cache.load().application_states
            maxcost = 0
            maxpath = "Error"
            searchdata = {} 

            for path in self.deps.iterkeys():
                if self.rec_fn(path, searchdata) > maxcost:
                    maxcost = self.rec_fn(path, searchdata)
                    maxpath = path

            #logging.debug("Max Path {} has cost {}".format(maxpath, maxcost))
            logging.info("Timing Estimates Loaded")
            return {
                'maxtime' : maxcost,
                'maxpath' : maxpath
            }
        except Exception as e:
            logging.exception(e)


    def rec_fn(self, path, searchdata):
        #init internal search data
        data = searchdata.get(path, None)
        if data is None:
            data = {'time':None, 'cost':None}
            searchdata.update({path:data})

        if data.get('cost', None) is not None:
            return data['cost']

        #look up running or graphite time
        if(self.states.get(path, None) is not None
           and self.states[path].get('application_status', None) is not None
           and self.states[path]['application_status'] == "running"):
            data['time'] =  0
        else: #not running, fetch graphite
            data['time'] = self.get_graphtite_data(path)

        #recurse into deps
        dep_data = self.deps.get(path, None)
        if dep_data is None:
            #logging.debug("Path {} has no dep_data".format(path))
            ret = 0
        elif len(dep_data['dependencies']) == 0:
            ret = 0
        else:
            ret = 0
            for iter in dep_data['dependencies']:
                if iter.get('type').lower() == DependencyType.CHILD:
                    ret = max(ret, self.rec_fn(iter.get("path", None), searchdata))
                if iter.get('type').lower() == DependencyType.GRANDCHILD:
                    grand_path = iter.get("path")
                    for key in self.deps.iterkeys():
                        if(key.lower().startswith(grand_path) and key.lower() != grand_path):
                            ret = max(ret, self.rec_fn(key, searchdata))

        data['cost'] = ret + data['time']

        return data['cost']

    def get_graphtite_data(self, path):
        if self.graphite_cache.get(path, None) is not None:
            return self.graphite_cache[path];

        try:
            url = path.split('/spot/software/state/')[1]
            url = url.replace('/', '.')
            #aggregateLine defaults to average
            url = 'http://'+self.configuration.graphite_host + '/render?target=aggregateLine(Infrastructure.startup.' + url + '.runtime)&format=json&from=-5d'
            response = requests.post(url, timeout=5.0)
            if response.status_code != httplib.OK:
                #logging.debug(url + " Has no graphite Data")
                self.graphite_cache[path] = 0
                return 0
            else:
                #first and only entry, it's first and only data point, and formatted as [ data, time ]
                self.graphite_cache[path] = response.json()[0]['datapoints'][0][0]

            return self.graphite_cache[path]

        except Exception as e:
            logging.exception(e)
            return 0
