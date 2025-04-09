from ._BaseHandler import BaseHandler

class MaterialManager(BaseHandler):
    def __init__(self):
        self.materials = {}

    def handles(self):
        return ["uniaxialMaterial"]

    def handle(self, func_name, arg_map):
        tag = int(arg_map["matTag"])
        mat_type = arg_map["matType"]
        params = arg_map["args"]
        self.materials[tag] = {"type": mat_type, "params": params}

    def clear(self):
        self.materials.clear()
