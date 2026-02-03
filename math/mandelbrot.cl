#ifdef cl_khr_fp64
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#elif defined(cl_amd_fp64)
    #pragma OPENCL EXTENSION cl_amd_fp64 : enable
#endif

#define ESCAPE_RADIUS2 4.0

__kernel void mandelbrot_kernel(
    __global float* escape_values,
    const double x_min,
    const double y_min,
    const double x_step,
    const double y_step,
    const int width,
    const int height,
    const int max_iterations,
    const double zoom_depth,
    const double z_real_offset,
    const double z_imag_offset

) { 
    
    double pixel_scale = fmax(fabs(x_step), fabs(y_step));
    int fidelity_cap = (int)(1000.0 * log2(1.0 / pixel_scale)); // tune multiplier as needed
    fidelity_cap = min(fidelity_cap, max_iterations); // enforce upper bound
    
    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);
    if (gid_x >= width || gid_y >= height) return;

    double c_real = x_min + gid_x * x_step;
    double c_imag = y_min + gid_y * y_step;
    double z_real = z_real_offset;
    double z_imag = z_imag_offset;

    int iteration = 0;
    double zr2 = 0.0;
    double zi2 = 0.0;

    while (zr2 + zi2 < ESCAPE_RADIUS2 && iteration < fidelity_cap) {
        double temp = zr2 - zi2 + c_real;
        z_imag = 2.0 * z_real * z_imag + c_imag;
        z_real = temp;
        zr2 = z_real * z_real;
        zi2 = z_imag * z_imag;
        iteration++;
    }

    double norm = iteration - log2(log2(zr2 + zi2)) + 4.0;
    norm = clamp(norm / max_iterations, 0.0, 1.0);

    double phase = log10(zoom_depth) - floor(log10(zoom_depth));
    double t = fmod(norm + phase, 1);

    escape_values[gid_y * width + gid_x] = (float)t;

}
