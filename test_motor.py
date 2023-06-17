from class_StepperMotor_controls_NiMax import StepperMotor


DIR_pin = "Dev1/port0/line3"
PUL_pin = "Dev1/ctr3"
pulse_count = 9500
low_duration = 600 * 10**-6
high_duration = 600 * 10**-6

motor = StepperMotor(DIR_pin, PUL_pin, pulse_count, low_duration, high_duration)

try:
    motor.start_motor()
    motor.rotate_direction(True) # direcion=True for CW, direction=False for CCW
    
    # Add a delay or other necessary operations here if needed

except KeyboardInterrupt:  # Press Ctrl+C to stop the code
    pass

finally:
    motor.stop_motor()  # Ensure motor is stopped before closing tasks
    