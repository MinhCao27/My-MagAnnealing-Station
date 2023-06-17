import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


# DRV5053VA specs
sensitivity = -0.009  # [V/G]
zeroField_voltage = 1  # [V]

# Set the channel name for the analog input
channel_x = "Dev1/ai0"
channel_y = "Dev1/ai1"

# If the polarity is positive (south pole),
# the voltage difference will be negative,
# so the magnetic field strength will be negative as well.
# If the polarity is negative (north pole),
# the voltage difference will be positive,
# resulting in a positive magnetic field strength.
def read_analog_voltage(channel):
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(channel)
        task.timing.cfg_samp_clk_timing(rate=100, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        task.start()
        
        while True:
            analog_voltage = task.read()
            yield analog_voltage

# Convert analog voltage to voltage in Gauss
def magnetic_field_conv(analog_voltage):
    voltage_diff = analog_voltage - zeroField_voltage
    magField_strength = voltage_diff / sensitivity
    return magField_strength

# Plot vectors in real time
def live_vectorPlot(frame):
    # Read the analog voltage from the sensors
    analog_voltage_x = next(read_analog_voltage(channel_x))
    analog_voltage_y = next(read_analog_voltage(channel_y))

    # Convert analog voltage to magnetic field strength
    magField_x = magnetic_field_conv(analog_voltage_x)
    magField_y = magnetic_field_conv(analog_voltage_y)

    # Total magnetic field properties
    totalField_magnitude = np.sqrt(magField_x**2 + magField_y**2)
    angle_theta_rad = np.arctan2(magField_y, magField_x)
    angle_theta_deg = np.degrees(angle_theta_rad)
    if angle_theta_deg < 0:
        angle_theta_deg += 360
    angle_theta_deg = angle_theta_deg % 360

    # Print the voltage and magnetic field values
    print("Voltage:     x-axis: {:10.4f} V   y-axis: {:10.4f} V\n"
          "Mag. Field:  x-axis: {:10.4f} G   y-axis: {:10.4f} G"
          .format(analog_voltage_x, analog_voltage_y, magField_x, magField_y))

    # Calculate the start points of the vectors
    x_start = 0
    y_start = 0
    x_end = magField_x
    y_end = magField_y

    # Set the axis limits based on the maximum magnitude
    max_magnitude = max(abs(magField_x), abs(magField_y))
    # ax.set_xlim([-2.5 * max_magnitude, 2.5 * max_magnitude]) # Live-adjusted axis range
    # ax.set_ylim([-2.5 * max_magnitude, 2.5 * max_magnitude])
    ax.set_xlim([-300, 300]) # Predetermined axis range
    ax.set_ylim([-300, 300])

    # Update the quiver plot
    quiver.set_offsets([[x_start, y_start]])
    quiver.set_UVC(x_end, y_end)
    quiver2.set_offsets([[x_start, y_start]])
    quiver2.set_UVC(magField_x, magField_y)

    # Update the text box with live data
    text_box.set_text("x-dir: {:6.2f} G\ny-dir: {:6.2f} G\nTotal: {:6.2f} G\n"
                      "$\Theta$ = {:.2f}$^\circ$"
                      .format(magField_x, magField_y, totalField_magnitude,
                              angle_theta_deg))

    # Remove previous angle patch
    if len(ax.patches) > 0:
        ax.patches[-1].remove()

    # Add angle notation dynamically
    angle_radius = max_magnitude * 0.8
    angle_patch = patches.Arc((0, 0), angle_radius, angle_radius,
                          angle=0, theta1=0, theta2=angle_theta_deg, color='red', linewidth=1.5)
    ax.add_patch(angle_patch)
    

    return quiver, quiver2, text_box

# Plotting vector addition function
fig, ax = plt.subplots()
ax.set_title('Real-time Magnetic Field Vector [G]')
ax.set_xlabel('x-axis')
ax.set_ylabel('y-axis')
# Add horizontal and vertical lines at x=0 and y=0
ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
ax.axvline(0, color='gray', linestyle='--', linewidth=0.5)

# Initialize the quiver plots
quiver = ax.quiver([0], [0], [0], [0], angles='xy', scale_units='xy', scale=1)
quiver2 = ax.quiver([0], [0], [0], [0], angles='xy', scale_units='xy',
                    color='b', scale=1)

# Create a separate ax object for the data box
data_box_ax = fig.add_axes([0.75, 0.8, 0.2, 0.1])
data_box_ax.axis("off")
text_box = data_box_ax.text(0.25, 0.00, "", ha="center", va="center", fontsize=10)

# Animate the plot
ani = animation.FuncAnimation(fig, live_vectorPlot, interval=100, cache_frame_data=False)

plt.show()

