def handle_fractal_interaction(mouse_pos, is_right_click_held, current_kernel, screen_to_complex):
    """
    Updates fractal rendering based on user interaction.
    
    Parameters:
        mouse_pos: tuple(x, y) of screen coordinates
        is_right_click_held: boolean indicating if right click is active
        current_kernel: one of 'mandelbrot', 'julia', or 'phoenix'
        screen_to_complex: function converting screen position to complex (c_real, c_imag)
    
    Returns:
        kernel_to_render: kernel function reference
        c_seed: tuple(c_real, c_imag) or None
    """
    # Convert screen to complex plane coordinates
    c_real, c_imag = screen_to_complex(mouse_pos)

    # Determine alternate fractal to render
    if is_right_click_held:
        if current_kernel == 'mandelbrot':
            return julia_kernel, (c_real, c_imag)
        elif current_kernel == 'julia':
            return mandelbrot_kernel, (c_real, c_imag)
        elif current_kernel == 'phoenix':
            # You could switch to a Julia form or custom Phoenix variant
            return julia_kernel, (c_real, c_imag)
    else:
        # Return current fractal without modifying seed
        return current_kernel, None

def screen_to_complex(mouse_x, mouse_y, view_rect, resolution):
    """Maps screen coordinates to complex plane coordinates."""
    x_min, x_max, y_min, y_max = view_rect
    width, height = resolution
    c_real = x_min + (mouse_x / width) * (x_max - x_min)
    c_imag = y_min + (mouse_y / height) * (y_max - y_min)
    return c_real, c_imag