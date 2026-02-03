from PyQt6.QtCore import Qt

def mousePressEvent(runtime, event):
    if event.button() == Qt.MouseButton.LeftButton:
        runtime.last_mouse_pos = event.position()
        runtime.mouse_pressed = True

def mouseReleaseEvent(runtime, event):
    if event.button() == Qt.MouseButton.LeftButton:
        runtime.mouse_pressed = False

def mouseMoveEvent(runtime, event):
    if runtime.mouse_pressed and runtime.last_mouse_pos is not None:
        dx = event.position().x() - runtime.last_mouse_pos.x()
        dy = event.position().y() - runtime.last_mouse_pos.y()
        x_range = runtime.x_max - runtime.x_min
        y_range = runtime.y_max - runtime.y_min
        x_offset = dx * x_range / runtime.width
        y_offset = dy * y_range / runtime.height
        runtime.x_min += x_offset
        runtime.x_max += x_offset
        runtime.y_min += y_offset
        runtime.y_max += y_offset
        runtime.last_mouse_pos = event.position()
        runtime.target_x_min = runtime.x_min
        runtime.target_x_max = runtime.x_max
        runtime.target_y_min = runtime.y_min
        runtime.target_y_max = runtime.y_max

def wheelEvent(runtime, event):
    pos = event.position()
    x_range = runtime.x_max - runtime.x_min
    y_range = runtime.y_max - runtime.y_min

    runtime.zoom_center_x = pos.x() / runtime.width
    runtime.zoom_center_y = pos.y() / runtime.height

    raw_delta = event.angleDelta().y()
    wheel_input = raw_delta / 300
    runtime.last_wheel_input = wheel_input

    if runtime.smooth_zoom_enabled:
        # Inject momentum only if input is meaningful
        if abs(wheel_input) > 0.001:
            runtime.zoom_momentum += wheel_input * runtime.zoom_acceleration
            runtime.zoom_momentum = max(-runtime.max_zoom_velocity,
                                    min(runtime.max_zoom_velocity, runtime.zoom_momentum))
            runtime.is_animating = True

    else:
        # Direct zoom path
        adjusted_factor = runtime.zoom_factor
        if abs(wheel_input) < 0.1:adjusted_factor *= 3.5
        zoom_scalar = 1.0 / 137 - (wheel_input * adjusted_factor)
        zoom_scalar = max(0.01, min(10.0, zoom_scalar))

        zoom_x = runtime.x_min + runtime.zoom_center_x * x_range
        zoom_y = runtime.y_min + runtime.zoom_center_y * y_range

        new_x_range = x_range * zoom_scalar
        new_y_range = y_range * zoom_scalar

        runtime.x_min = zoom_x - new_x_range * runtime.zoom_center_x
        runtime.x_max = zoom_x + new_x_range * (1.0 - runtime.zoom_center_x)
        runtime.y_min = zoom_y - new_y_range * runtime.zoom_center_y
        runtime.y_max = zoom_y + new_y_range * (1.0 - runtime.zoom_center_y)

        runtime.target_x_min = runtime.x_min
        runtime.target_x_max = runtime.x_max
        runtime.target_y_min = runtime.y_min
        runtime.target_y_max = runtime.y_max
