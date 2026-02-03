

__kernel void colorize_kernel(
    __global float* escape_values,
    __global uchar4* output,
    const int width,
    const int height,
    const float t,
    const float phase,
    const float freq,
    const float sat,
    const float val,
    const int mode
) {
    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);
    if (gid_x >= width || gid_y >= height) return;

    int idx = gid_y * width + gid_x;
    float norm = clamp(escape_values[idx], 0.0f, 1.0f);

    uchar4 color;
    switch (mode) {
        case 0: color = sinebow(norm, phase, freq, sat, val); break;
        case 1: color = sinebowxl(norm, phase, freq, sat, val); break;
        case 2: color = bluedive(norm, phase, freq, sat, val); break;
        case 3: color = grayscale(norm, phase, freq, sat, val); break;
        default: color = (uchar4)(0, 0, 0, 255); break;
    }

    output[idx] = color;
}