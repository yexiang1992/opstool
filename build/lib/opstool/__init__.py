from .__about__ import __version__
from .utils import load_ops_examples
from . import vis, preprocessing, analysis


membs = dict()
for mod in (vis, preprocessing, analysis):
    for name in mod.__all__:
        if hasattr(mod, name):
            membs[name] = getattr(mod, name)
cur_dict = globals()
cur_dict.update(membs)
membs_all = vis.__all__ + preprocessing.__all__ + analysis.__all__

__all__ = [
    "load_ops_examples",
    "__version__",
] + membs_all
