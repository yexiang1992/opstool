from collections import defaultdict
import inspect, types, functools
from _manager import BaseHandler, NodeManager, ElementManager, MaterialManager, LoadManager, TimeSeriesManager

class OpenSeesSpy:
    def __init__(self, module):
        self.module = module
        self.call_log = defaultdict(list)
        self.original_functions = {}

        # Register handlers here
        self.handlers: list[BaseHandler] = [
            NodeManager(),
            ElementManager(),
            MaterialManager(),
            TimeSeriesManager(),
            LoadManager()
        ]

        # Build a dispatch table: func_name -> handler
        self.dispatch_table = {}
        for handler in self.handlers:
            for name in handler.handles():
                self.dispatch_table[name] = handler

    def hook_all(self):
        for name in dir(self.module):
            attr = getattr(self.module, name)
            if isinstance(attr, (types.FunctionType, types.BuiltinFunctionType)):
                self._hook_function(name, attr)

    def _hook_function(self, name, func):
        self.original_functions[name] = func

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            arg_map = {"args": args, "kwargs": kwargs}

            self.call_log[name].append(arg_map)

            # Dispatch to handler
            handler = self.dispatch_table.get(name)
            if handler:
                print(name, arg_map)
                handler.handle(name, arg_map)

            return func(*args, **kwargs)

        setattr(self.module, name, wrapper)

    def restore_all(self):
        for name, func in self.original_functions.items():
            setattr(self.module, name, func)
        self.original_functions.clear()

    def clear(self):
        self.call_log.clear()
        for handler in self.handlers:
            handler.clear()


if __name__ == '__main__':
    import openseespy.opensees as ops
    import matplotlib.pyplot as plt

    # 假设你已经有下面这些类
    # - OpenSeesSpy
    # - NodeManager(BaseHandler)
    # - ElementManager(BaseHandler)
    # ...（参考前文）

    # 创建 spy 并挂钩所有命令
    spy = OpenSeesSpy(ops)
    spy.hook_all()

    # 运行 OpenSees 命令
    ops.model("basic", "-ndm", 2, "-ndf", 3)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.node(3, 1.0, 1.0)
    ops.node(4, 0.0, 1.0)

    # 提取节点数据
    node_dict = spy.handlers[0].nodes

    # 准备画图数据
    x_coords = []
    y_coords = []
    labels = []

    for tag, coords in node_dict.items():
        x_coords.append(coords[0])
        y_coords.append(coords[1])
        labels.append(str(tag))

    # 绘图
    plt.figure(figsize=(5, 5))
    plt.scatter(x_coords, y_coords, c='blue', s=60)

    # 添加标签
    for i, txt in enumerate(labels):
        plt.text(x_coords[i] + 0.02, y_coords[i] + 0.02, txt, fontsize=10)

    plt.title("OpenSees Node Layout")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True)
    plt.show()

