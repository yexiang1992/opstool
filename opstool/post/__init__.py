import os
import shutil
from .model_data import save_model_data, load_model_data
from .eigen_data import save_eigen_data, load_eigen_data, get_eigen_data
from .responses_data import CreateODB, loadODB, get_nodal_responses, get_element_responses, get_model_data
from ..utils import CONSTANTS

RESULTS_DIR = CONSTANTS.get_output_dir()

if not os.path.exists(RESULTS_DIR):
    os.mkdir(RESULTS_DIR)

def set_odb_path(path: str):
    CONSTANTS.set_output_dir(path)
    for item in os.listdir(RESULTS_DIR):
        source_path = os.path.join(RESULTS_DIR, item)
        target_path = os.path.join(path, item)
        shutil.move(source_path, target_path)
    shutil.rmtree(RESULTS_DIR)


__all__ = [
    "set_odb_path",
    "save_model_data",
    "save_eigen_data",
    "load_model_data",
    "load_eigen_data",
    "get_eigen_data",
    "CreateODB",
    "loadODB",
    "get_model_data",
    "get_nodal_responses",
    "get_element_responses"
]
