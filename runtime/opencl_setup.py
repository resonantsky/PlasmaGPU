import pyopencl as cl
import numpy as np
import sys
import shutil
import os
from .kernel_loader import build_program


def initialize_opencl(self):
    """Initializes OpenCL context, device, buffers, and kernel program."""
    clear_opencl_cache()

    # 🎯 Select GPU device (fallback to first platform if AMD not found)
    platforms = cl.get_platforms()
    self.platform = next((p for p in platforms if "AMD" in p.name.upper()), platforms[0])

    try:
        self.device = self.platform.get_devices(device_type=cl.device_type.GPU)[0]
    except (IndexError, cl.RuntimeError) as e:
        print("❌ OpenCL GPU not found:", e)
        sys.exit(1)

    # 🧠 Create OpenCL context and command queue
    self.context = cl.Context(devices=[self.device])
    self.queue = cl.CommandQueue(self.context)

    # 📐 Work group tuning
    self.work_group_size = 8
    build_options = [f"-D WORK_GROUP_SIZE={self.work_group_size}"]

    # 🔧 Build OpenCL kernels
    self.program = build_program(self.context, build_options=build_options)

    # 📏 Image dimensions and buffer sizes
    self.output_shape = (self.height, self.width, 4)  # RGBA layout
    buf_size_rgba = np.prod(self.output_shape).item()  # total bytes for uchar4 image

    # 🎨 Output image buffer
    self.output_array = np.zeros(self.output_shape, dtype=np.uint8)
    self.output_buffer = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, size=buf_size_rgba)

    # 🌀 Escape values buffer (float32 precision)
    self.escape_array = np.zeros((self.height, self.width), dtype=np.float32)
    self.escape_buffer = cl.Buffer(self.context, cl.mem_flags.READ_WRITE, size=self.escape_array.nbytes)

def clear_opencl_cache():
    """Backs up and clears the PyOpenCL cache to force kernel rebuild."""
    try:
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "pyopencl")
        backup_dir = cache_dir + ".bak"
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        if os.path.exists(cache_dir):
            os.rename(cache_dir, backup_dir)
    except Exception:
        pass