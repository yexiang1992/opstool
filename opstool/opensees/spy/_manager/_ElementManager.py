from ._BaseHandler import BaseHandler

class ElementManager(BaseHandler):
    def __init__(self):
        self.elements = {}

    def handles(self):
        return ["element"]

    def handle(self, func_name, arg_map):
        tag = int(arg_map["tag"])
        typeName = arg_map["typeName"]
        args = arg_map["args"] if "args" in arg_map else []

        handler = getattr(self, f"_handle_{typeName}", self._handle_default)
        self.elements[tag] = handler(tag, *args)

    def _handle_default(self, tag, *args):
        return {"type": "Unknown", "nodes": list(map(int, args[:2]))}

    def _handle_Truss(self, tag, *args):
        return {
            "type": "Truss",
            "nodes": list(map(int, args[:2])),
            "A": float(args[2]),
            "matTag": int(args[3])
        }

    def clear(self):
        self.elements.clear()

