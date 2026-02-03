from .kernel_config import get_color_args
import numpy as np


def get_kernel_args(widget, runtime):
    mode = widget.fractal_mode

    kernel_name = {
        0: "mandelbrot_kernel",
        1: "julia_kernel",
        2: "newton_kernel",
        3: "phoenix_kernel"
    }[mode]

    x_range = runtime.x_max - runtime.x_min
    y_range = runtime.y_max - runtime.y_min
    x_step = x_range / runtime.width
    y_step = y_range / runtime.height

    # Use seed offsets written to runtime during mode switch
    z_real_offset = runtime.z_real_offset
    z_imag_offset = runtime.z_imag_offset

    if mode == 0:  # Mandelbrot
        args = [
            runtime.escape_buffer,
            np.float64(runtime.x_min),
            np.float64(runtime.y_min),
            np.float64(x_step),
            np.float64(y_step),
            np.int32(runtime.width),
            np.int32(runtime.height),
            np.int32(runtime.max_iterations),
            np.float64(runtime.zoom_depth),
            np.float64(z_real_offset),
            np.float64(z_imag_offset)
        ]

    elif mode == 1:  # Julia
        args = [
            runtime.escape_buffer,
            np.float64(runtime.x_min),
            np.float64(runtime.y_min),
            np.float64(x_step),
            np.float64(y_step),
            np.int32(runtime.width),
            np.int32(runtime.height),
            np.int32(runtime.max_iterations),
            np.float64(runtime.zoom_depth),
            np.float64(z_real_offset),
            np.float64(z_imag_offset)
        ]

    elif mode == 2:  # Newton
        args = [
            runtime.escape_buffer,
            np.float64(runtime.x_min),
            np.float64(runtime.y_min),
            np.float64(x_step),
            np.float64(y_step),
            np.int32(runtime.width),
            np.int32(runtime.height),
            np.int32(runtime.max_iterations),
            np.float64(1e-6),  # convergence_epsilon
            np.float64(runtime.zoom_depth),
            np.float64(z_real_offset),
            np.float64(z_imag_offset)
        ]

    elif mode == 3:  # Phoenix
        args = [
            runtime.escape_buffer,
            np.float64(runtime.x_min),
            np.float64(runtime.y_min),
            np.float64(x_step),
            np.float64(y_step),
            np.int32(runtime.width),
            np.int32(runtime.height),
            np.int32(runtime.max_iterations),
            np.float64(runtime.zoom_depth),
            np.float64(z_real_offset),
            np.float64(z_imag_offset)
        ]

    else:
        raise ValueError(f"Unknown fractal mode: {mode}")

    return kernel_name, args