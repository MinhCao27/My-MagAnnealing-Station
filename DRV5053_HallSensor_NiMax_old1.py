from class_DRV5053VA_HallSensor_NiMax_combined import DRV5053VA_HallSensor_NiMax_combined


### -------- Hall Sensors -------- ###
xDir_sensor = "Dev1/ai0"
yDir_sensor = "Dev1/ai1"
HallSensors = DRV5053VA_HallSensor_NiMax_combined(xDir_sensor, yDir_sensor)
HallSensors.start_animation()
