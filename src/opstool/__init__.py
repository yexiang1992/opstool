from .__about__ import __version__
from .utils import load_ops_examples
from .vis import *
from .analysis import *
from .preprocessing import *
from . import vis, preprocessing, analysis


_membs = dict()
for mod in (vis, preprocessing, analysis):
    for name in mod.__all__:
        if hasattr(mod, name):
            _membs[name] = getattr(mod, name)
cur_dict = globals()
cur_dict.update(_membs)
_membs_all = vis.__all__ + preprocessing.__all__ + analysis.__all__

__all__ = [
    "load_ops_examples",
    "__version__",
] + _membs_all
