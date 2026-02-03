import os
import pyopencl as cl

DEFAULT_KERNEL_DIR = os.path.join(os.path.dirname(__file__), "..", "math")

def load_kernel_sources(kernel_dir=DEFAULT_KERNEL_DIR):
    ordered_files = [
        "gradients.cl",
        "colorize_kernel.cl",
        "mandelbrot.cl",
        "julia.cl",
        "newton.cl",
        "phoenix.cl"
        
    ]
    sources = []
    for filename in ordered_files:
        path = os.path.join(kernel_dir, filename)
        print(f"➜ {filename}")
        with open(path, "r") as f:
            sources.append(f.read())
    return "\n".join(sources)

def build_program(context, kernel_dir=DEFAULT_KERNEL_DIR, build_options=None):
    source_code = load_kernel_sources(kernel_dir)
    print("\n✅\n")
    build_opts = " ".join(build_options) if build_options else ""
    try:
        return cl.Program(context, source_code).build(options=build_opts)
    except cl.RuntimeError as e:
        print("❌ OpenCL build failed.")
        for device in context.devices:
            log = cl.Program(context, source_code).get_build_info(device, cl.program_build_info.LOG)
            print(f"Build log for {device.name}:\n{log}")
        raise