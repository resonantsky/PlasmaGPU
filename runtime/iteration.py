import numpy as np
from PyQt6.QtCore import Qt
from .render_fractal import render_fractal

def adjust_iterations_by_scale(self):
    # --- Zoom Analysis ---
    x_zoom = self.base_width / (self.x_max - self.x_min)
    y_zoom = self.base_height / (self.y_max - self.y_min)
    zoom_level = max(1.0, max(x_zoom, y_zoom))

    # --- Iteration Scaling ---
    min_iter, max_iter = 10, 10000
    norm_zoom = min(1.0, np.log10(zoom_level) / np.log10(1e8))
    sensitivity = 1.618
    target_iterations = int(min_iter + (max_iter - min_iter) * (norm_zoom ** sensitivity))

    # --- Performance Factor ---
    performance_factor = 1.0
    if len(self.frame_time_history) >= 10:
        median_time = sorted(self.frame_time_history[-10:])[5]
        desired_time = self.target_frame_time * self.target_load_factor

        if median_time > 0:
            if median_time > desired_time * 1.1:
                performance_factor = min(desired_time / median_time, 0.9)
            elif median_time < desired_time * 0.8 and self.frame_time_stable:
                performance_factor = min(desired_time / median_time, 1.2)

            target_iterations = int(target_iterations * performance_factor)
            target_iterations = max(min_iter, min(max_iter, target_iterations))

    # --- Apply Iteration Change ---
    if self.max_iterations != target_iterations:
        change = target_iterations - self.max_iterations
        limited = int(change * self.iteration_change_rate)
        if limited == 0 and change != 0:
            limited = 1 if change > 0 else -1
        new_iterations = max(min_iter, min(max_iter, self.max_iterations + limited))

        if abs(new_iterations - self.max_iterations) > 2:
            self.max_iterations = new_iterations
            self.iterations_spinbox.setText(str(self.max_iterations))

    return self.max_iterations

def update_iterations_from_zoom(self):
    if not self.scaled_iterations_enabled:
        return

    # --- Zoom Mapping ---
    zoom = self.base_width / (self.x_max - self.x_min)
    zmin, zmax = self.scaled_min_zoom, self.scaled_max_zoom
    imin, imax = self.scaled_min_iterations, self.scaled_max_iterations

    if zoom <= zmin:
        self.max_iterations = imin
    elif zoom >= zmax:
        self.max_iterations = imax
    else:
        t = (np.log10(zoom) - np.log10(zmin)) / (np.log10(zmax) - np.log10(zmin))
        self.max_iterations = int(imin + (imax - imin) * t)

    self.iterations_spinbox.setText(str(self.max_iterations))

def update_iterations(self, value):
    self.max_iterations = value
    self.render_fractal()

def toggle_scaled_iterations(self, state):
    enabled = (state == Qt.CheckState.Checked.value)
    self.scaled_iterations_enabled = enabled

    self.scaled_min_edit.setEnabled(enabled)
    self.scaled_max_edit.setEnabled(enabled)
    self.iterations_spinbox.setEnabled(not enabled)

    if enabled:
        self.update_iterations_from_zoom()

    self.render_fractal()

def update_scaled_iterations(self):
    try:
        imin = int(self.scaled_min_edit.text())
        imax = int(self.scaled_max_edit.text())
        if imin < 10 or imax < imin:
            return
        self.scaled_min_iterations = imin
        self.scaled_max_iterations = imax

        self.update_iterations_from_zoom()
        self.render_fractal()

    except ValueError:
        pass