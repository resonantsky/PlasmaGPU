from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QPushButton,
    QLineEdit, QDoubleSpinBox, QLabel, QCheckBox
)
from PyQt6.QtCore import Qt
from .fractal_gl import FractalGLWidget 
from .iteration import update_scaled_iterations
from .mode_switch import update_color_params, reset_view, toggle_smooth_zoom

def setup_ui(self):
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    self.fractal_display = FractalGLWidget(runtime=self, parent=self)
    self.fractal_display.setMinimumSize(self.width, self.height)
    self.fractal_display.setFocus()
    main_layout.addWidget(self.fractal_display)
    control_layout = QHBoxLayout()
    control_layout.setContentsMargins(10, 10, 10, 10)
    
    iterations_label = QLabel("Iterations:")
    iterations_label.setMaximumWidth(100)
    self.iterations_spinbox = QLineEdit(str(self.max_iterations))
    self.iterations_spinbox.setMaximumWidth(60)
    self.iterations_spinbox.setReadOnly(self.scaled_iterations_enabled)
    control_layout.addWidget(iterations_label)
    control_layout.addWidget(self.iterations_spinbox)
    self.scaled_min_edit = QLineEdit(str(self.scaled_min_iterations))
    self.scaled_max_edit = QLineEdit(str(self.scaled_max_iterations))
    self.scaled_min_edit.setMaximumWidth(50)
    self.scaled_max_edit.setMaximumWidth(50)
    self.scaled_min_edit.returnPressed.connect(self.update_scaled_iterations)
    self.scaled_max_edit.returnPressed.connect(self.update_scaled_iterations)
    control_layout.addWidget(self.scaled_min_edit)
    control_layout.addWidget(self.scaled_max_edit)

   

    control_container = QWidget()
    control_container.setLayout(control_layout)
    control_container.setObjectName("ControlContainer")
    self.fractal_selector = QComboBox()
    self.fractal_selector.addItems(["Mandelbrot", "Julia", "Newtonian", "Phoenix"])
    self.fractal_selector.setCurrentIndex(self.fractal_mode)
    self.fractal_selector.currentIndexChanged.connect(self.fractal_display.change_fractal_mode)
    control_layout.addWidget(self.fractal_selector)

    # Color mode selector
    self.color_mode_dropdown = QComboBox()
    self.color_mode_dropdown.addItems(["Tie-Dye", "Psychedelic", "Blue Dive", "Moon Landing"])
    self.color_mode_dropdown.setToolTip("Select coloring mode")
    self.color_mode_dropdown.setMaximumWidth(150)
    self.color_mode_dropdown.currentIndexChanged.connect(self.set_color_mode)

    # Unified color parameter controls
    self.color_t_spin = QDoubleSpinBox()
    self.color_t_spin.setPrefix("t: ")
    self.color_t_spin.setRange(-1.0, 1.0)
    self.color_t_spin.setDecimals(3)
    self.color_t_spin.setSingleStep(0.01)
    self.color_t_spin.setValue(self.color_t)
    self.color_t_spin.setToolTip("Set to -1 to use computed t, or set a value [0,1] for fixed color position.")
    self.color_t_spin.valueChanged.connect(self.update_color_params)
    self.color_t_spin.setVisible(False)  # Optional: hide unless needed
    self.color_phase_spin = QDoubleSpinBox()
    self.color_phase_spin.setSuffix(" Phase")
    self.color_phase_spin.setRange(-10.0, 10.0)
    self.color_phase_spin.setDecimals(3)
    self.color_phase_spin.setSingleStep(0.001)
    self.color_phase_spin.setValue(self.color_phase)
    self.color_phase_spin.valueChanged.connect(self.update_color_params)
    self.color_freq_spin = QDoubleSpinBox()
    self.color_freq_spin.setSuffix(" Frequency")
    self.color_freq_spin.setRange(0.01, 10.0)
    self.color_freq_spin.setDecimals(3)
    self.color_freq_spin.setSingleStep(0.01)
    self.color_freq_spin.setValue(self.color_freq)
    self.color_freq_spin.valueChanged.connect(self.update_color_params)
    self.color_sat_spin = QDoubleSpinBox()
    self.color_sat_spin.setSuffix(" Saturation")
    self.color_sat_spin.setRange(0.0, 10.0)
    self.color_sat_spin.setDecimals(3)
    self.color_sat_spin.setSingleStep(0.01)
    self.color_sat_spin.setValue(self.color_sat)
    self.color_sat_spin.valueChanged.connect(self.update_color_params)
    self.color_val_spin = QDoubleSpinBox()
    self.color_val_spin.setSuffix(" Value")
    self.color_val_spin.setRange(0.0, 10.0)
    self.color_val_spin.setDecimals(3)
    self.color_val_spin.setSingleStep(0.01)
    self.color_val_spin.setValue(self.color_val)
    self.color_val_spin.valueChanged.connect(self.update_color_params)

    self.z_real_edit = QDoubleSpinBox()
    self.z_imag_edit = QDoubleSpinBox()

    # Configure precision and bounds
    self.z_real_edit.setMaximumWidth(160)
    self.z_imag_edit.setMaximumWidth(160)
    self.z_real_edit.setDecimals(6)
    self.z_imag_edit.setDecimals(6)
    self.z_real_edit.setRange(-10.0, 10.0)
    self.z_imag_edit.setRange(-10.0, 10.0)
    self.z_real_edit.setSingleStep(0.0001)
    self.z_imag_edit.setSingleStep(0.0001)

    # Bind handler
   
    self.z_real_edit.setValue(self.z_real_offset)
    self.z_imag_edit.setValue(self.z_imag_offset)
    self.z_real_edit.valueChanged.connect(self.update_z_offsets)
    self.z_imag_edit.valueChanged.connect(self.update_z_offsets)
    
    # Add to layout
    control_layout.addWidget(self.z_real_edit)
    control_layout.addWidget(self.z_imag_edit)
    # Add widgets to layout
    control_layout.addWidget(self.color_mode_dropdown)
    control_layout.addWidget(self.color_phase_spin)
    control_layout.addWidget(self.color_freq_spin)
    control_layout.addWidget(self.color_sat_spin)
    control_layout.addWidget(self.color_val_spin)
    #control_layout.addWidget(self.set_escape_radius_spin)

    self.reset_button = QPushButton("Reset View")
    self.reset_button.clicked.connect(self.reset_view)
    control_layout.addWidget(self.reset_button)

    self.smooth_zoom_checkbox = QCheckBox("Smooth Zoom")
    self.smooth_zoom_checkbox.setChecked(self.smooth_zoom_enabled)
    self.smooth_zoom_checkbox.stateChanged.connect(self.toggle_smooth_zoom)
    control_layout.addWidget(self.smooth_zoom_checkbox)

    main_layout.addWidget(control_container)

    # Create the widgets
    
    
       

    
    # Read initial values

    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    self.setCentralWidget(central_widget)