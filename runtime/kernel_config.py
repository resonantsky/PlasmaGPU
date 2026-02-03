# kernel_config.py
import numpy as np
DEFAULT_SINEBOW = {
    "t": -0.001,
    "phase": 1.0,
    "freq": 2.0,
    "sat": 1.0,
    "val": 1.0
}

CONVERGENCE_EPSILON = 1e-10
MAX_ITERATIONS = 10000
DEFAULT_WORK_GROUP_SIZE = None
MAX_ZOOM_DEPTH = 1e308

def get_color_args(runtime):
    return [
    np.int32(runtime.width),
    np.int32(runtime.height),
    np.float32(runtime.color_t),
    np.float32(runtime.color_phase),
    np.float32(runtime.color_freq),
    np.float32(runtime.color_sat),
    np.float32(runtime.color_val),
    np.int32(runtime.color_mode),
]
