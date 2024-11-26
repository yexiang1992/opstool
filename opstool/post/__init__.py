import  os
from .model_data import save_model_data, load_model_data
from .eigen_data import save_eigen_data, load_eigen_data, get_eigen_data
from .responses_data import CreateODB, loadODB, get_nodal_responses, get_element_responses
from ..utils import RESULTS_DIR

if not os.path.exists(RESULTS_DIR):
    os.mkdir(RESULTS_DIR)


__all__ = [
    "save_model_data",
    "save_eigen_data",
    "load_model_data",
    "load_eigen_data",
    "get_eigen_data",
    "CreateODB",
    "loadODB",
    "get_nodal_responses",
    "get_element_responses"
]
