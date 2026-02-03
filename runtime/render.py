
import pyopencl as cl 
def enqueue_kernel(runtime, kernel_name, scalar_args, buffers=[]):
    
    # Retrieve the kernel function from the compiled OpenCL program
    
    if kernel_name not in runtime.kernels:
        runtime.kernels[kernel_name] = cl.Kernel(runtime.program, kernel_name)

    kernel = runtime.kernels[kernel_name]
    
    # getattr(runtime.program, kernel_name) dynamically fetches the compiled kernel from the runtime.
    
    # Combine buffer arguments (typically GPU memory) and scalar parameters
    
    kernel_args = buffers + scalar_args
    
    # buffers + scalar_args orders arguments to match the kernel signature.
    
    # Define the size of the global work grid (e.g. total number of threads)
    
    global_size = (runtime.width, runtime.height)
    
    # global_size sets the full compute grid (e.g. pixels or shader fragments).
    
    # Define the size of each local work group (i.e. subgroup of threads)
    
    local_size = (runtime.work_group_size, runtime.work_group_size)
    
    # local_size sets the parallelism chunk size for optimization.
    
    # Enqueue the kernel for execution on the OpenCL command queue
    
    kernel(runtime.queue, global_size, local_size, *kernel_args)
    
    #  Final line dispatches work to the GPU via OpenCL.


    
   
    
    
