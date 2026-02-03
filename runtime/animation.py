from PyQt6.QtCore import QTimer
from .fps import update_fps
from .iteration import update_iterations_from_zoom, adjust_iterations_by_scale
from .render_fractal import render_fractal

def apply_zoom_at_point(x_min, x_max, y_min, y_max, zoom_factor, center_x, center_y, base_width):
    x_range = x_max - x_min
    y_range = y_max - y_min
    new_x_range = x_range / zoom_factor
    new_y_range = y_range / zoom_factor
    x_offset = (x_range - new_x_range) * center_x
    y_offset = (y_range - new_y_range) * center_y
    new_x_min = x_min + x_offset
    new_x_max = new_x_min + new_x_range
    new_y_min = y_min + y_offset
    new_y_max = new_y_min + new_y_range
    zoom_depth = base_width / new_x_range if new_x_range > 0 else 1.0
    return new_x_min, new_x_max, new_y_min, new_y_max, zoom_depth

def setup_timers(self):
    self.animation_timer = QTimer()
    self.animation_timer.timeout.connect(self.animation_step)
    self.animation_timer.start(1)  

def animation_step(self):
    # Frame timing update and smoothing
    elapsed = self.frame_timer.elapsed()
    frame_time = elapsed - self.last_frame_time
    self.last_frame_time = elapsed
    self.frame_time_history.append(frame_time)
    if len(self.frame_time_history) > self.frame_time_history_size:
        self.frame_time_history.pop(0)

    # Smooth zoom momentum update
    if abs(self.zoom_momentum) > self.min_zoom_velocity and self.smooth_zoom_enabled:
        zoom_factor = 1.0 + self.zoom_momentum
        (self.x_min, self.x_max,
         self.y_min, self.y_max,
         self.zoom_depth) = apply_zoom_at_point(
            self.x_min, self.x_max,
            self.y_min, self.y_max,
            zoom_factor,
            self.zoom_center_x, self.zoom_center_y,
            self.width
        )

        # Update zoom targets and dampen momentum
        self.target_x_min = self.x_min
        self.target_x_max = self.x_max
        self.target_y_min = self.y_min
        self.target_y_max = self.y_max
        self.zoom_momentum *= self.zoom_decay
        self.zoom_momentum = 0.0 if abs(self.zoom_momentum) < 1e-9 else \
            max(-self.max_zoom_velocity, min(self.max_zoom_velocity, self.zoom_momentum))
        self.is_animating = self.zoom_momentum != 0.0

    # Positional animation toward target bounds
    elif self.is_animating:
        self.x_min += (self.target_x_min - self.x_min) * self.animation_speed
        self.x_max += (self.target_x_max - self.x_max) * self.animation_speed
        self.y_min += (self.target_y_min - self.y_min) * self.animation_speed
        self.y_max += (self.target_y_max - self.y_max) * self.animation_speed

        total_shift = (
            abs(self.target_x_min - self.x_min) +
            abs(self.target_x_max - self.x_max) +
            abs(self.target_y_min - self.y_min) +
            abs(self.target_y_max - self.y_max)
        )
        if total_shift < 1e-10:
            self.x_min, self.x_max = self.target_x_min, self.target_x_max
            self.y_min, self.y_max = self.target_y_min, self.target_y_max
            self.is_animating = False

    # Iteration adjustment logic based on settings
    if self.scaled_iterations_enabled:
        update_iterations_from_zoom(self)
    elif self.adapt_iterations:
        adjust_iterations_by_scale(self)
    else:
        # Manual mode: read from input box but don't force write unless empty or invalid
        # This prevents breaking the user's typing experience
        try:
            val_text = self.iterations_spinbox.text()
            if val_text:
                value = int(val_text)
                self.max_iterations = min(max(value, 10), 10000)
        except ValueError:
            pass

    # Trigger final render and frame increment
    render_fractal(self)
    self.frame_count += 1
