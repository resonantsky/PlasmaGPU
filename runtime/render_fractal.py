from .get_kernel_args import get_kernel_args       # Retrieves appropriate kernel name and arguments based on UI state
from .colorize import run_colorize_kernel          # Applies coloring to the fractal based on escape time or iteration data
from PyQt6.QtGui import QImage                     # Handles conversion of rendered data to displayable image
import numpy as np                                 # Provides data types and array utilities used in OpenCL buffer exchange
import pyopencl as cl                              # Interface for OpenCL GPU computation



def render_fractal(self):
    
    # Compute pixel step sizes
    x_range = self.x_max - self.x_min
    y_range = self.y_max - self.y_min
    x_step = x_range / self.width
    y_step = y_range / self.height

    # Define thread layout for GPU compute
    global_size = (self.width, self.height) 
    local_size = (self.work_group_size, self.work_group_size)

    # Get fractal kernel and arguments based on user-selected mode
    
    self.kernels = {}

    kernel_name, kernel_args = get_kernel_args(self.fractal_display, self)

    if kernel_name not in self.kernels:
        self.kernels[kernel_name] = cl.Kernel(self.program, kernel_name)

    fractal_kernel = self.kernels[kernel_name]
    fractal_kernel(self.queue, global_size, local_size, *kernel_args)

    # Colorization pass: map escape values to final visual color
    run_colorize_kernel(self, self.escape_buffer, self.output_buffer)

    cl.enqueue_copy(self.queue, self.output_array, self.output_buffer)
    self.has_prev_frame = False

    # Convert GPU output into a displayable Qt image and update GUI
    img = QImage(self.output_array.data, self.width, self.height, QImage.Format.Format_RGBA8888)
    self.fractal_display.set_fractal_image(img)
    
  