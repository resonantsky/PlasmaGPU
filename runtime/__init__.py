from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from .state import initialize_state
from .opencl_setup import initialize_opencl
from .ui_setup import setup_ui
from .animation import setup_timers, animation_step
from .iteration import update_scaled_iterations
from .mode_switch import update_color_params, set_color_mode, reset_view, toggle_smooth_zoom
from .render_fractal import render_fractal

 

class PlasmaMandelbrotViewer(QMainWindow):
    
    def sync_offset_controls(self, z_real: float = None, z_imag: float = None):
        """Sync spinboxes from explicit values, or fall back to instance vars."""
        real_val = z_real if z_real is not None else self.z_real_offset
        imag_val = z_imag if z_imag is not None else self.z_imag_offset

        self.z_real_edit.setValue(real_val)
        self.z_imag_edit.setValue(imag_val)


    def update_z_offsets(self):
        self.z_real_offset = float(self.z_real_edit.text())
        self.z_imag_offset = float(self.z_imag_edit.text())
        

    def __init__(self, parent=None):
        super().__init__(parent)
        initialize_state(self)
        initialize_opencl(self)
        
    

        self.has_prev_frame = False
        self.render_callback = lambda: render_fractal(self)
        
        # Zoom and interaction state
        self.last_mouse_pos = None
        self.mouse_pressed = False
        self.smooth_zoom_enabled = True
        self.set_escape_radius = 2.0
        
        self.last_wheel_input = 0.0 
        self.zoom_acceleration = 0.001
        self.max_zoom_velocity = 2.0
        self.zoom_factor = 0.1
        self.zoom_decay = 1.0 - 1e-4
        
     
  

        # Functional bindings
        self.update_scaled_iterations = lambda: update_scaled_iterations(self)
        self.update_color_params = lambda: update_color_params(self)
        self.set_color_mode = lambda index: set_color_mode(self, index)
        self.reset_view = lambda: reset_view(self)
        self.toggle_smooth_zoom = lambda state: toggle_smooth_zoom(self, state)
        

        # Optional if you want redraw separation
        #self.set_escape_radius = lambda value: set_escape_radius(self, value)
        # UI setup
        setup_ui(self)

        # Connect unified color controls
        self.color_t_spin.valueChanged.connect(self.update_color_params)
        self.color_phase_spin.valueChanged.connect(self.update_color_params)
        self.color_freq_spin.valueChanged.connect(self.update_color_params)
        self.color_sat_spin.valueChanged.connect(self.update_color_params)
        self.color_val_spin.valueChanged.connect(self.update_color_params)
        self.z_real_edit.valueChanged.connect(self.update_z_offsets)
        self.z_imag_edit.valueChanged.connect(self.update_z_offsets)
        self.z_real_edit.blockSignals(True)
        self.z_imag_edit.blockSignals(True)
        self.z_imag_edit.setValue(self.z_imag_offset)
        self.z_real_edit.setValue(self.z_real_offset)
        
        
        self.z_real_edit.blockSignals(False)
        self.z_imag_edit.blockSignals(False)
        # Connect mode selector
        self.color_mode_dropdown.currentIndexChanged.connect(self.set_color_mode)

        # Animation loop
        self.animation_step = lambda: animation_step(self)
        setup_timers(self)
    
        