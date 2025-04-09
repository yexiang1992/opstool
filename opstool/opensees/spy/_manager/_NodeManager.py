from ._BaseHandler import BaseHandler

class NodeManager(BaseHandler):
    def __init__(self):
        self.nodes = {}

    def handles(self):
        return ["node"]

    def handle(self, func_name, arg_map):
        args = arg_map["args"]
        tag = int(args[0])
        coords = args[1:]
        self.nodes[tag] = coords

    def _handle_mass(self, arg_map):
        args = arg_map["args"]
        mass = self._extract_args_by_str(args, ["-mass", "-Mass"])

    def clear(self):
        self.nodes.clear()
