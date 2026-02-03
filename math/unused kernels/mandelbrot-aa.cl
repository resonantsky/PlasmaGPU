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
    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);
    if (gid_x >= width || gid_y >= height) return;

    // Pixel center
    double c_real = x_min + gid_x * x_step;
    double c_imag = y_min + gid_y * y_step;

    // Supersampling: 2x2 grid per pixel (4 samples)
    const int samples = 4;
    double total_norm = 0.0;
    int sample_count = 0;

    // Offset in pixel space: 0.25, 0.75 for 2x2
    const double offsets[4][2] = {
        {-0.25, -0.25},  // bottom-left
        {+0.25, -0.25},  // bottom-right
        {-0.25, +0.25},  // top-left
        {+0.25, +0.25}   // top-right
    };

    for (int s = 0; s < samples; s++) {
        double dx = offsets[s][0] * x_step;
        double dy = offsets[s][1] * y_step;

        double zr = z_real_offset;
        double zi = z_imag_offset;
        double cr = c_real + dx;
        double ci = c_imag + dy;

        int iter = 0;
        double zr2 = zr * zr;
        double zi2 = zi * zi;

        while (zr2 + zi2 < ESCAPE_RADIUS2 && iter < max_iterations) {
            double temp = zr2 - zi2 + cr;
            zi = 2.0 * zr * zi + ci;
            zr = temp;
            zr2 = zr * zr;
            zi2 = zi * zi;
            iter++;
        }

        // Smooth coloring with log
        double norm = iter;
        if (iter < max_iterations) {
            double log_zn = log2(log2(zr2 + zi2));
            norm = iter - log2(log_zn) + 4.0;
        }
        norm = clamp(norm / max_iterations, 0.0, 1.0);

        total_norm += norm;
        sample_count++;
    }

    // Average the samples
    double avg_norm = total_norm / sample_count;

    // Add phase shift based on zoom depth (preserved)
    double phase = log10(zoom_depth) - floor(log10(zoom_depth));
    double t = fmod(avg_norm + phase, 1.0);

    // Store result (same as before)
    escape_values[gid_y * width + gid_x] = (float)t;
}
