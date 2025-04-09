from ._BaseHandler import BaseHandler

class LoadManager(BaseHandler):
    def __init__(self):
        self.patterns = {}

    def handles(self):
        return ["uniaxialMaterial"]

    def handle(self, func_name, arg_map):
        tag = int(arg_map["matTag"])
        mat_type = arg_map["matType"]
        params = arg_map["args"]
        self.patterns[tag] = {"type": mat_type, "params": params}

    def clear(self):
        self.patterns.clear()


class TimeSeriesManager:
    def __init__(self):
        self.series = {}

    def handles(self):
        return ["uniaxialMaterial"]

    def handle(self, func_name, arg_map):
        tag = int(arg_map["matTag"])
        mat_type = arg_map["matType"]
        params = arg_map["args"]
        self.series[tag] = {"type": mat_type, "params": params}

    def clear(self):
        self.series.clear()