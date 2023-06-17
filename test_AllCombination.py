from class_DRV5053VA_HallSensor_NiMax import DRV5053VA_HallSensor_NiMax
from class_StepperMotor_controls_NiMax import StepperMotor
import time
import threading



### -------- Hall Sensors -------- ###
# xDir_sensor = "Dev1/ai0"
# yDir_sensor = "Dev1/ai1"
# HallSensor_x = DRV5053VA_HallSensor_NiMax(xDir_sensor)
# HallSensor_y = DRV5053VA_HallSensor_NiMax(yDir_sensor)

# HallSensor_x.start_hall_sensor()
# HallSensor_y.start_hall_sensor()

# magField_x = HallSensor_x.get_magnetic_field()
# magField_y = HallSensor_y.get_magnetic_field()

# # Plotting the fields
# HallSensors = DRV5053VA_HallSensor_NiMax_plot(magField_x, magField_y)
# HallSensors.start_animation()



#----------------------------------------------------------#
#----------------------------------------------------------#


### ------- Stepper Motors ------- ###

# Pulse setup
rev_count = 10 # 5 revolutions move distance of 1cm
pulse_count = 200 * rev_count # Driver is set to 200 pulses/rev, so pulse_count determines number of revolutions
low_duration = 600 * 10**-6
high_duration = 600 * 10**-6

# xPlus motor
DIR_pin_xPlus = "Dev1/port0/line0"
PUL_pin_xPlus = "Dev1/ctr0"
motor_xPlus = StepperMotor(DIR_pin_xPlus, PUL_pin_xPlus, rev_count, pulse_count, low_duration, high_duration)

# xMinus motor
DIR_pin_xMinus = "Dev1/port0/line1"
PUL_pin_xMinus = "Dev1/ctr1"
motor_xMinus = StepperMotor(DIR_pin_xMinus, PUL_pin_xMinus, rev_count, pulse_count, low_duration, high_duration)

# yPlus motor
DIR_pin_yPlus = "Dev1/port0/line2"
PUL_pin_yPlus = "Dev1/ctr2"
motor_yPlus = StepperMotor(DIR_pin_yPlus, PUL_pin_yPlus, rev_count, pulse_count, low_duration, high_duration)

# yMinus motor
DIR_pin_yMinus = "Dev1/port0/line3"
PUL_pin_yMinus = "Dev1/ctr3"
motor_yMinus = StepperMotor(DIR_pin_yMinus, PUL_pin_yMinus, rev_count, pulse_count, low_duration, high_duration)


# Function to run motor tasks
def run_motor_task(motor, direction):
    motor.start_motor()
    motor.rotate_direction(direction)
    # motor.stop_motor()


# Start the motor tasks concurrently
motor_threads = []
direction = True  # direction=True for CW, direction=False for CCW
num_iterations = pulse_count // 10  # Number of iterations based on pulse_count

try:
    for i in range(num_iterations):
        # Create and start thread for each motor task
        motor_threads.append(threading.Thread(target=run_motor_task, args=(motor_xPlus, direction)))
        motor_threads.append(threading.Thread(target=run_motor_task, args=(motor_xMinus, direction)))
        motor_threads.append(threading.Thread(target=run_motor_task, args=(motor_yPlus, direction)))
        motor_threads.append(threading.Thread(target=run_motor_task, args=(motor_yMinus, direction)))

        # Start the threads
        for thread in motor_threads:
            thread.start()

        # Wait for all threads to finish
        for thread in motor_threads:
            thread.join()

        # Clear the list for the next iteration
        motor_threads = []
        time.sleep(1)
    
    
except KeyboardInterrupt:  # Press Ctrl+C to interrupt the code
    print("Crtl+C")
        

finally:  # All tasks are ensured to be stopped and closed properly
    print("Finally")
    time.sleep(1)
    for motor in [motor_xPlus, motor_xMinus, motor_yPlus, motor_yMinus]:
        motor.stop_motor()
