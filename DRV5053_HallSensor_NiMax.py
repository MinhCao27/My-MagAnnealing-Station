from class_DRV5053VA_HallSensor_NiMax import DRV5053VA_HallSensor_NiMax
from class_DRV5053VA_HallSensor_NiMax import magneticField_plot2D
import threading

### -------- Hall Sensors -------- ###
xDir_sensor = "Dev1/ai0"
yDir_sensor = "Dev1/ai1"
HallSensor_x = DRV5053VA_HallSensor_NiMax(xDir_sensor)
HallSensor_y = DRV5053VA_HallSensor_NiMax(yDir_sensor)

def run_hallSensor_task(hallSensor):
    hallSensor.start_hall_sensor()
    magField = hallSensor.get_magnetic_field()
    
hallSensor_threads = []


try:
    hallSensor_threads.append(threading.Thread(target=run_hallSensor_task, args=(HallSensor_x,)))
    hallSensor_threads.append(threading.Thread(target=run_hallSensor_task, args=(HallSensor_y,)))
    
    # Start all the motor_threads
    for thread in hallSensor_threads:
        thread.start()
    
    # Wait for all motor threads to complete
    for thread in hallSensor_threads:
        thread.join()
    
finally:
    for hallSensor in [HallSensor_x, HallSensor_y]:
        hallSensor.stop_hall_sensor()

# Plotting the fields
# HallSensors = magneticField_plot2D(magField_x, magField_y)
# HallSensors.start_animation()
