from class_DRV5053VA_HallSensor_NiMax import DRV5053VA_HallSensor_NiMax
from class_DRV5053VA_HallSensor_NiMax_plot import DRV5053VA_HallSensor_NiMax_plot
from class_StepperMotor_controls_NiMax import StepperMotor
# from class_LimitSwitch_NiMax import LimitSwitch
import time
import threading



### -------- Hall Sensors -------- ###
xDir_sensor = "Dev1/ai0"
yDir_sensor = "Dev1/ai1"
HallSensor_x = DRV5053VA_HallSensor_NiMax(xDir_sensor)
HallSensor_y = DRV5053VA_HallSensor_NiMax(yDir_sensor)

# HallSensor_x.start_hall_sensor()
# HallSensor_y.start_hall_sensor()

# magField_x = HallSensor_x.get_magnetic_field()
# magField_y = HallSensor_y.get_magnetic_field()

# # Plotting the fields
# HallSensors = DRV5053VA_HallSensor_NiMax_plot(magField_x, magField_y)
# HallSensors.start_animation()



#----------------------------------------------------------#
#----------------------------------------------------------#



# ### ------- Limit Switches ------- ###
# switch_xPlus_near = LimitSwitch("Dev1/port0/line24")
# switch_xPlus_far = LimitSwitch("Dev1/port0/line25")

# switch_xMinus_near = LimitSwitch("Dev1/port0/line26")
# switch_xMinus_far = LimitSwitch("Dev1/port0/line27")

# switch_yPlus_near = LimitSwitch("Dev1/port0/line28")
# switch_yPlus_far = LimitSwitch("Dev1/port0/line29")

# switch_yMinus_near = LimitSwitch("Dev1/port0/line30")
# switch_yMinus_far = LimitSwitch("Dev1/port0/line31")



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


# Start the 4 motors' motion when asked by the user
def get_user_input(prompt, valid_inputs):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_inputs:
            return user_input
        else:
            print("Invalid input. Please re-enter ({})".format("/".join(valid_inputs)))

# Get the magnetic field specifications from the user            
def get_magnetic_field_inputs():
    print("Final magnetic field you would like to obtain:")
    desired_totalField_magnitude = float(input("   \u2022 Total field magnitude: "))
    desired_theta = float(input("   \u2022 Angle \u03F4 (measured from x-axis): "))
    return desired_totalField_magnitude, desired_theta


# # Moving the magnets to their original calibrated positions
# def calibrated_position():
    # value_xPlus_far = switch_xPlus_far.read_limit_switch()
    # value_xMinus_far = switch_xMinus_far.read_limit_switch()
    # value_yPlus_far = switch_yPlus_far.read_limit_switch()
    # value_yMinus_far = switch_yMinus_far.read_limit_switch()

    # # Create a threading event for each motor to signal when it has reached its calibrated position
    # motor_xPlus_calibrated = threading.Event()
    # motor_xMinus_calibrated = threading.Event()
    # motor_yPlus_calibrated = threading.Event()
    # motor_yMinus_calibrated = threading.Event()

    # # Define a function to check if all motors have reached their calibrated positions
    # def check_all_motors_calibrated():
        # if all(
            # value_xPlus_far, value_xMinus_far, value_yPlus_far, value_yMinus_far
        # ):
            # motor_xPlus_calibrated.set()
            # motor_xMinus_calibrated.set()
            # motor_yPlus_calibrated.set()
            # motor_yMinus_calibrated.set()

    # # Start the thread to check if all motors have reached their calibrated positions
    # check_thread = threading.Thread(target=check_all_motors_calibrated)
    # check_thread.start()

    # # Rotate the motors simultaneously until they reach their calibrated positions
    # motor_xPlus.rotate_direction(False)
    # motor_xMinus.rotate_direction(False)
    # motor_yPlus.rotate_direction(False)
    # motor_yMinus.rotate_direction(False)

    # # Wait for each motor to reach its calibrated position
    # motor_xPlus_calibrated.wait()
    # motor_xMinus_calibrated.wait()
    # motor_yPlus_calibrated.wait()
    # motor_yMinus_calibrated.wait()

    # # Stop the motors after reaching the calibrated positions
    # motor_xPlus.stop_motor()
    # motor_xMinus.stop_motor()
    # motor_yPlus.stop_motor()
    # motor_yMinus.stop_motor()

    # # Join the check thread to ensure it has finished
    # check_thread.join()


# Moving the magnets from the original calibrated positions to their desired positions    
def desired_motor_positions(magField_x, magField_y, desired_totalField_magnitude, desired_theta):
    # Calculate the required magnitudes of x and y components
    desired_magField_x = desired_totalField_magnitude * np.cos(np.radians(desired_theta))
    desired_magField_y = desired_totalField_magnitude * np.sin(np.radians(desired_theta))

    # Set the desired tolerance for magnitude and theta
    magnitude_tolerance = 0.1

    # Create threading events for each motor to signal when they have reached their desired positions
    motor_xPlus_reached = threading.Event()
    motor_xMinus_reached = threading.Event()
    motor_yPlus_reached = threading.Event()
    motor_yMinus_reached = threading.Event()

    # Define a function to move the motors based on the magnetic field readings
    def move_motors():
        nonlocal magField_x, magField_y

        # Adjust the motor movements until the desired positions are reached
        while (
            abs(magField_x - desired_magField_x) > magnitude_tolerance or
            abs(magField_y - desired_magField_y) > magnitude_tolerance
        ):
            # Move motor_xPlus
            if magField_x < desired_magField_x:
                motor_xPlus.rotate_direction(True)
            else:
                motor_xPlus.rotate_direction(False)

            # Move motor_xMinus
            if magField_x > desired_magField_x:
                motor_xMinus.rotate_direction(True)
            else:
                motor_xMinus.rotate_direction(False)

            # Move motor_yPlus
            if magField_y < desired_magField_y:
                motor_yPlus.rotate_direction(True)
            else:
                motor_yPlus.rotate_direction(False)

            # Move motor_yMinus
            if magField_y > desired_magField_y:
                motor_yMinus.rotate_direction(True)
            else:
                motor_yMinus.rotate_direction(False)

            # Update the magnetic field readings
            magField_x, magField_y = HallSensor.get_magnetic_field()

        # Stop all motors once the desired positions are reached
        motor_xPlus.stop_motor()
        motor_xMinus.stop_motor()
        motor_yPlus.stop_motor()
        motor_yMinus.stop_motor()

        # Signal that all motors have reached their desired positions
        motor_xPlus_reached.set()
        motor_xMinus_reached.set()
        motor_yPlus_reached.set()
        motor_yMinus_reached.set()

    # Start the thread for motor movement
    motor_thread = threading.Thread(target=move_motors)
    motor_thread.start()

    # Wait for all motors to reach their desired positions
    motor_xPlus_reached.wait()
    motor_xMinus_reached.wait()
    motor_yPlus_reached.wait()
    motor_yMinus_reached.wait()

    # Join the motor thread to ensure it has finished
    motor_thread.join()


while True:
    # Prompt for motor movement confirmation
    valid_movement_inputs = ["yes", "no", "y", "n"]
    movement_input = get_user_input("Do you want to start moving the motors? (Yes/No): ", valid_movement_inputs)

    if movement_input in ["yes", "y"]:
        # Prompt for magnetic field specifications
        desired_totalField_magnitude, desired_theta = get_magnetic_field_inputs()
        
        # Prompt for sample operation choice
        valid_operation_inputs = ["efficient", "e", "spiral", "s"]
        operation_input = get_user_input("   \u2022 Getting Magnetic Field: 'Efficient' or 'Spiral': ", valid_operation_inputs)


        if operation_input in ["efficient", "e"]:
            print("Starting motor: Taking efficient path...")
            
            try:
                HallSensor_x.start_hall_sensor()
                HallSensor_y.start_hall_sensor()
                magField_x = HallSensor_x.get_magnetic_field()
                magField_y = HallSensor_y.get_magnetic_field()
                
                desired_motor_positions(magField_x, magField_y, desired_totalField_magnitude, desired_theta)
            
            # except KeyboardInterrupt:  # Press Ctrl+C to interrupt the code
                # HallSensor.stop_hall_sensors()
                # for motor in [motor_xPlus, motor_xMinus, motor_yPlus, motor_yMinus]:
                    # motor.stop_motor() # Stop all motors if interrupted
                    
            finally:
                HallSensor_x.stop_hall_sensor()
                HallSensor_y.stop_hall_sensor()
                
                for motor in [motor_xPlus, motor_xMinus, motor_yPlus, motor_yMinus]:
                    motor.stop_motor() # Stop all motors if interrupted

            
        elif operation_input in ["spiral", "s"]:
            print("Starting motor: Taking spiral path...")
            # Perform operation here
            #
            #
            
        else:
            print("Invalid input. No operation will be performed.")


        # Message to print after the motors have reached their desired position
        print("Final position achieved.")

    else:
        print("Motor movement canceled.")

    print()  # Print an empty line for clarity
