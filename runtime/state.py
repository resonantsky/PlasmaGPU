from PyQt6.QtCore import Qt, QTimer, QElapsedTimer
def initialize_state(self):
    self.setMouseTracking(True)
    self.setWindowTitle("PlasmaMandelbrot Explorer v1.8c")
    screen = self.screen() or self.window().screen()
    self.width = screen.size().width()
    self.height = screen.size().height()
    self.resize(self.width, self.height)

    self.fractal_mode = 0
    self.x_min = -2.5
    self.x_max = 1.0
    self.y_min = -1.0
    self.y_max = 1.0
    self.max_iterations = 900
    self.color_t = -1.0
    self.color_phase = 0.0
    self.color_freq = 1.0
    self.color_sat = 1.0
    self.color_val = 1.0
    self.color_mode = 0  # Default to Sinebow

    self.target_x_min = self.x_min
    self.target_x_max = self.x_max
    self.target_y_min = self.y_min
    self.target_y_max = self.y_max
    self.is_animating = False
    self.animation_speed = 0.001
    self.smooth_zoom_enabled = True
    self.zoom_momentum = 0.001
    self.zoom_decay = 0.999
    self.zoom_acceleration = 0.001
    self.max_zoom_velocity = 0.05
    self.min_zoom_velocity = 0.001
    self.zoom_center_x = 0.0
    self.zoom_center_y = 0.0

    self.frame_timer = QElapsedTimer()
    self.frame_timer.start()
    self.last_frame_time = 0
    self.frame_time = 1
    self.target_frame_time = 1
    self.frame_time_history = []
    self.frame_time_history_size = 30
    self.frame_time_stable = True
    self.adapt_iterations = False
    self.max_possible_iterations = 10000
    self.iteration_change_rate = 0.001
    self.last_adjustment_time = 0
    self.adjustment_cooldown = 500
    self.target_load_factor = 0.00

    self.scaled_iterations_enabled = True
    self.scaled_min_iterations = 0
    self.scaled_max_iterations = 1000
    self.scaled_min_zoom = 1.0
    self.scaled_max_zoom = 7.6e13

    self.base_width = 3.5
    self.base_height = 2.0
    self.zoom_depth = 1.0
    self.show_precision_info = True
    self.max_zoom_depth = 1e308

    self.mouse_pressed = False
    self.zoom_factor = 0.1

    self.julia_mode = False
    self.z_real_offset = 0.0
    self.z_imag_offset = 0.0
    


    self.frame_counter = 0
    self.frame_count = 0
    self.fps = 0

