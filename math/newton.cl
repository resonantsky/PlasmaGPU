#ifdef cl_khr_fp64
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#elif defined(cl_amd_fp64)
    #pragma OPENCL EXTENSION cl_amd_fp64 : enable
#endif

#define ESCAPE_RADIUS2 4.0
#define ROOT_EPSILON 0.001

__kernel void newton_kernel(
    __global float* escape_values,
    const double x_min,
    const double y_min,
    const double x_step,
    const double y_step,
    const int width,
    const int height,
    const int max_iterations,
    const double convergence_epsilon,
    const double zoom_depth,
    const double z_real_offset,
    const double z_imag_offset
) {
    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);
    if (gid_x >= width || gid_y >= height) return;

    double z_real = x_min + gid_x * x_step + z_real_offset;
    double z_imag = y_min + gid_y * y_step + z_imag_offset;

    int iteration = 0;
    double delta = 1.0;
    double orbit_sum = 0.0;

    while (iteration < max_iterations && delta > convergence_epsilon) {
        double z_r2 = z_real * z_real;
        double z_i2 = z_imag * z_imag;

        double z_r3 = z_real * z_r2 - 3.0 * z_real * z_i2;
        double z_i3 = 3.0 * z_r2 * z_imag - z_imag * z_i2;

        double f_r = z_r3 - 1.0;
        double f_i = z_i3;

        double dz_r = 3.0 * (z_r2 - z_i2);
        double dz_i = 6.0 * z_real * z_imag;

        double denom = dz_r * dz_r + dz_i * dz_i;
        double nr = (f_r * dz_r + f_i * dz_i) / denom;
        double ni = (f_i * dz_r - f_r * dz_i) / denom;

        z_real -= nr;
        z_imag -= ni;

        delta = nr * nr + ni * ni;

        // Local orbit field: higher harmonic distortion
        orbit_sum += cos(z_real * 1.7) * sin(z_imag * 2.3);

        iteration++;
    }

    double norm = pow((double)iteration / (double)max_iterations, 0.5);
    norm = clamp(norm, 0.0, 1.618);

    // Modulate escape value by orbit texture and zoom phase
    double phase = fmod(log2(zoom_depth), -1.0);
    double detail = sin(orbit_sum * 0.00);

    double t = fmod(norm + detail * 0.3 + phase, 1.0);
    escape_values[gid_y * width + gid_x] = (float)t;
}