#ifndef GRADIENTS_CL
#define GRADIENTS_CL

// Shared constants
#define PI 3.14159265f
#define TAU 6.2831853f



// Sinebow coloring
uchar4 sinebow(float t, float phase, float freq, float sat, float val) {
    //float angle = TAU * (t * (freq + phase));
    float angle = TAU * (t * (freq + phase));
    float r = 0.5f * (sin(angle) + 1.0f);
    float g = 0.5f * (sin(angle + 2.0943951f) + 1.0f);
    float b = 0.5f * (sin(angle + 4.1887902f) + 1.0f);
    float l = 0.5f * fmax(fmax(r, g), fmin(fmin(r, g), b));
    r = l + (r - l) * sat;
    g = l + (g - l) * sat;
    b = l + (b - l) * sat;
    r *= val; g *= val; b *= val;
    return (uchar4)(255.0f * r, 255.0f * g, 255.0f * b, 255);
}

// Sinebow coloring
uchar4 sinebowxl(float t, float phase, float freq, float sat, float val) {
    //float angle = TAU * (t * (freq + phase));
    float angle = TAU / (t * (freq + phase)); 
    float r = 0.5f * (sin(angle) + 1.0f);
    float g = 0.5f * (sin(angle + 2.0943951f) + 1.0f);
    float b = 0.5f * (sin(angle + 4.1887902f) + 1.0f);
    float l = 0.5f * fmax(fmax(r, g), fmin(fmin(r, g), b));
    r = l + (r - l) * sat;
    g = l + (g - l) * sat;
    b = l + (b - l) * sat;
    r *= val; g *= val; b *= val;
    return (uchar4)(255.0f * r, 255.0f * g, 255.0f * b, 255);
}

// Blue Dive coloring
uchar4 bluedive(float t, float phase, float freq, float sat, float val) {  
    float heat = clamp(pow(t, freq) + phase, 0.0f, 1.0f);
    float r = clamp(heat > 0.7f ? (heat - 0.7f) * 5.0f : 0.0f, 0.0f, 1.0f); 
    float g = clamp(heat > 0.3f ? (heat - 0.3f) * 1.5f : 0.0f, 0.0f, 1.0f); 
    float b = clamp(heat, 0.0f, 1.0f);

    return (uchar4)(
        255.0f * r,
        255.0f * g,
        255.0f * b,
        255
    );
}

// Grayscale coloring
uchar4 grayscale(float t, float phase, float freq, float sat, float val) {
    float gray = clamp(pow(t + phase, freq) * val, 0.0f, 1.0f);
    return (uchar4)(255.0f * gray, 255.0f * gray, 255.0f * gray, 255);
}


#endif