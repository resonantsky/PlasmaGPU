from .render import enqueue_kernel
from .kernel_config import get_color_args

def run_colorize_kernel(runtime, escape_buffer, output_buffer):
    color_args = get_color_args(runtime)
    enqueue_kernel(runtime, "colorize_kernel", scalar_args=color_args, buffers=[escape_buffer, output_buffer])