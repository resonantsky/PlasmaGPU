__kernel void frame_smooth_with_zoom(
    __global const uchar4* current, 
    __global const uchar4* previous,
    __global uchar4* output,
    const float alpha,
    const int width,
    const int height)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    if (x >= width || y >= height) return;

    int idx = y * width + x;

    uchar4 c = current[idx];
    uchar4 p = previous[idx];

    float u = (float)x / (float)width;
    float v = (float)y / (float)height;

    // Spatial envelope: wavelike + center focus
    float breath = 0.5f + 0.5f * sin(u * 6.2831f);     // ~ 2π → one wave
    float trail = 1.0f - fabs(v - 0.5f) * 2.0f;        // center peak

    float modulation = breath * trail;                 // -1 to +1
    float dynamic_alpha = clamp(alpha * (1.0f + 0.5f * modulation), 0.0f, 1.0f);

    // Blend channels
    float fx = dynamic_alpha * c.x + (1.0f - dynamic_alpha) * p.x;
    float fy = dynamic_alpha * c.y + (1.0f - dynamic_alpha) * p.y;
    float fz = dynamic_alpha * c.z + (1.0f - dynamic_alpha) * p.z;

    uchar4 out;
    out.x = (uchar)clamp(fx, 0.0f, 255.0f);
    out.y = (uchar)clamp(fy, 0.0f, 255.0f);
    out.z = (uchar)clamp(fz, 0.0f, 255.0f);
    out.w = 255;

    output[idx] = out;
}
