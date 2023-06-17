import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from nidaqmx.stream_readers import AnalogSingleChannelReader

class DRV5053VA_HallSensor_NiMax_combined:
    def __init__(self, channel_x, channel_y):
        # DRV5053VA specs
        self.sensitivity = -0.009  # [V/G]
        self.zeroField_voltage = 1  # [V]

        # Set the channel names for the analog inputs
        self.channel_x = channel_x
        self.channel_y = channel_y

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

    def read_analog_voltage(self, channel):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(channel)
            task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
            task.start()

            reader = AnalogSingleChannelReader(task.in_stream)

            while self.is_running:
                analog_voltage = reader.read_one_sample()
                yield analog_voltage
                
        
    def magnetic_field_conv(self, analog_voltage):
        voltage_diff = analog_voltage - self.zeroField_voltage
        magField_strength = voltage_diff / self.sensitivity
        return magField_strength
        
    def get_magnetic_field(self):
        analog_voltage_x = next(self.read_analog_voltage(self.channel_x))
        analog_voltage_y = next(self.read_analog_voltage(self.channel_y))
        magField_x = self.magnetic_field_conv(analog_voltage_x)
        magField_y = self.magnetic_field_conv(analog_voltage_y)
        return magField_x, magField_y
        
    def get_angle_theta(self, magField_x, magField_y):
        angle_theta_rad = np.arctan2(magField_y, magField_x)
        angle_theta_deg = np.degrees(angle_theta_rad)
        return angle_theta_deg

    def live_vectorPlot(self, frame):
        # analog_voltage_x = next(self.read_analog_voltage(self.channel_x))
        # analog_voltage_y = next(self.read_analog_voltage(self.channel_y))
        
        magField_x, magField_y = self.get_magnetic_field()
        totalField_magnitude = np.sqrt(magField_x ** 2 + magField_y ** 2)
        
        # print("Voltage:     x-axis: {:10.4f} V   y-axis: {:10.4f} V\n"
              # "Mag. Field:  x-axis: {:10.4f} G   y-axis: {:10.4f} G"
              # .format(analog_voltage_x, analog_voltage_y, magField_x, magField_y))

        angle_theta_deg = self.get_angle_theta(magField_x, magField_y)
        if angle_theta_deg < 0:
            angle_theta_deg += 360
        angle_theta_deg = angle_theta_deg % 360

        x_start = 0
        y_start = 0
        x_end = magField_x
        y_end = magField_y

        max_magnitude = max(abs(magField_x), abs(magField_y))
        # self.ax.set_xlim([-2.5 * max_magnitude, 2.5 * max_magnitude]) # Live-adjusted axis range
        # self.ax.set_ylim([-2.5 * max_magnitude, 2.5 * max_magnitude])
        self.ax.set_xlim([-300, 300]) # Predetermined axis range
        self.ax.set_ylim([-300, 300])

        self.quiver.set_offsets([[x_start, y_start]])
        self.quiver.set_UVC(x_end, y_end)
        self.quiver2.set_offsets([[x_start, y_start]])
        self.quiver2.set_UVC(magField_x, magField_y)

        self.text_box.set_text("x-dir: {:6.2f} G\ny-dir: {:6.2f} G\nTotal: {:6.2f} G\n"
                               "$\Theta$ = {:.2f}$^\circ$"
                               .format(magField_x, magField_y, totalField_magnitude, angle_theta_deg))

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
        ani = animation.FuncAnimation(self.fig, self.live_vectorPlot, interval=100, cache_frame_data=False)
        plt.show()

    def stop_hall_sensors(self):
        self.is_running = False
        
        # Stop and close the Analog Input tasks
        with nidaqmx.Task() as task_x, nidaqmx.Task() as task_y:
            task_x.ai_channels.add_ai_voltage_chan(self.channel_x)
            task_y.ai_channels.add_ai_voltage_chan(self.channel_y)
            
            task_x.stop()
            task_y.stop()
            
            task_x.close()
            task_y.close()
            