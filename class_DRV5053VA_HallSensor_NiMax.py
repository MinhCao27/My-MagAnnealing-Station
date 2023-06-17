import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


class DRV5053VA_HallSensor_NiMax:
    def __init__(self, channel):
        # DRV5053VA specs
        self.sensitivity = -0.009  # [V/G]
        self.zeroField_voltage = 1  # [V]
        
        self.channel = channel
        
        self.task = nidaqmx.Task()
        self.task.ai_channels.add_ai_voltage_chan(channel)
        self.task.timing.cfg_samp_clk_timing(rate=500, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
    
    def start_hall_sensor(self):
        self.task.start()
    
    def read_analog_voltage(self):
        while True:
            analog_voltage = self.task.read()
            return analog_voltage
            
    def magnetic_field_conv(self, analog_voltage):
        voltage_diff = analog_voltage - self.zeroField_voltage
        magField_strength = voltage_diff / self.sensitivity
        print("magField = ", magField_strength)
        return magField_strength
        
    def get_magnetic_field(self):
        analog_voltage = self.read_analog_voltage()
        magField = self.magnetic_field_conv(analog_voltage)
        return magField

    def stop_hall_sensor(self):
        # Stop and close the Analog Input tasks
        self.task.stop()
        self.task.close()
        
        
class magneticField_plot2D:
    def __init__(self, magField_x, magField_y):
        # Set the channel names for the magnetic field inputs
        self.magField_x = magField_x
        self.magField_y = magField_y

        # Initialize the plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Real-time Magnetic Field Vector [G]')
        self.ax.set_xlabel('x-axis')
        self.ax.set_ylabel('y-axis')
        self.ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)  # Add horizontal line at y=0
        self.ax.axvline(0, color='gray', linestyle='--', linewidth=0.5)  # Add vertical line at x=0

        # Initialize the quiver plots
        self.quiver = self.ax.quiver([0], [0], [0], [0], angles='xy', scale_units='xy', scale=1)
        self.quiver2 = self.ax.quiver([0], [0], [0], [0], angles='xy', scale_units='xy', color='b', scale=1)

        # Create a separate ax object for the data box
        self.data_box_ax = self.fig.add_axes([0.75, 0.8, 0.2, 0.1])
        self.data_box_ax.axis("off")
        self.text_box = self.data_box_ax.text(0.25, 0.00, "", ha="center", va="center", fontsize=10)
        
        # Variable to keep track of animation state
        self.is_running = False
                

    def get_angle_theta(self):
        angle_theta_rad = np.arctan2(self.magField_y, self.magField_x)
        angle_theta_deg = np.degrees(angle_theta_rad)
        return angle_theta_deg

    def live_vectorPlot(self, frame):
        # analog_voltage_x = next(self.read_analog_voltage(self.channel_x))
        # analog_voltage_y = next(self.read_analog_voltage(self.channel_y))
        
        # magField_x, magField_y = self.get_magnetic_field()
        totalField_magnitude = np.sqrt(self.magField_x ** 2 + self.magField_y ** 2)
        
        # print("Voltage:     x-axis: {:10.4f} V   y-axis: {:10.4f} V\n"
              # "Mag. Field:  x-axis: {:10.4f} G   y-axis: {:10.4f} G"
              # .format(analog_voltage_x, analog_voltage_y, self.magField_x, self.magField_y))

        angle_theta_deg = self.get_angle_theta()
        if angle_theta_deg < 0:
            angle_theta_deg += 360
        angle_theta_deg = angle_theta_deg % 360

        x_start = 0
        y_start = 0
        x_end = self.magField_x
        y_end = self.magField_y

        max_magnitude = max(abs(self.magField_x), abs(self.magField_y))
        # self.ax.set_xlim([-2.5 * max_magnitude, 2.5 * max_magnitude]) # Live-adjusted axis range
        # self.ax.set_ylim([-2.5 * max_magnitude, 2.5 * max_magnitude])
        self.ax.set_xlim([-300, 300]) # Predetermined axis range
        self.ax.set_ylim([-300, 300])

        self.quiver.set_offsets([[x_start, y_start]])
        self.quiver.set_UVC(x_end, y_end)
        self.quiver2.set_offsets([[x_start, y_start]])
        self.quiver2.set_UVC(self.magField_x, self.magField_y)

        self.text_box.set_text("x-dir: {:6.2f} G\ny-dir: {:6.2f} G\nTotal: {:6.2f} G\n"
                               "$\Theta$ = {:.2f}$^\circ$"
                               .format(self.magField_x, self.magField_y, totalField_magnitude, angle_theta_deg))

        if len(self.ax.patches) > 0:
            self.ax.patches[-1].remove()

        angle_radius = max_magnitude * 0.8
        angle_patch = patches.Arc((0, 0), angle_radius, angle_radius,
                                  angle=0, theta1=0, theta2=angle_theta_deg, color='red', linewidth=1.5)
        self.ax.add_patch(angle_patch)

        return self.quiver, self.quiver2, self.text_box

    def start_animation(self):
        if self.is_running:
            return
        self.is_running = True
        ani = animation.FuncAnimation(self.fig, self.live_vectorPlot, interval=500, cache_frame_data=False)
        plt.show()