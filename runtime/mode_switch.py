from PyQt6.QtCore import Qt
from .render_fractal import render_fractal

def toggle_smooth_zoom(self, state):
    self.smooth_zoom_enabled = Qt.CheckState(state) == Qt.CheckState.Checked

    # Don't inject momentum—let wheelEvent do that
    if self.smooth_zoom_enabled and abs(self.zoom_momentum) > self.min_zoom_velocity:
        self.is_animating = True
    else:
        self.is_animating = False

    render_fractal(self)


def reset_view(self):
    self.zoom_momentum = 0.0
    if self.smooth_zoom_enabled:
        self.target_x_min = -2.5
        self.target_x_max = 1.0
        self.target_y_min = -1.0
        self.target_y_max = 1.0
        self.is_animating = True
    else:
        self.x_min = -2.5
        self.x_max = 1.0
        self.y_min = -1.0
        self.y_max = 1.0
        self.target_x_min = self.x_min
        self.target_x_max = self.x_max
        self.target_y_min = self.y_min
        self.target_y_max = self.y_max

    self.zoom_center_x = 0.5
    self.zoom_center_y = 0.5
    render_fractal(self)

def set_color_mode(runtime, index):
    runtime.color_mode = index
    if hasattr(runtime, "render_callback"):
        runtime.render_callback()


def update_color_params(self):
    self.color_t = self.color_t_spin.value()
    self.color_phase = self.color_phase_spin.value()
    self.color_freq = self.color_freq_spin.value()
    self.color_sat = self.color_sat_spin.value()
    self.color_val = self.color_val_spin.value()
    render_fractal(self)

