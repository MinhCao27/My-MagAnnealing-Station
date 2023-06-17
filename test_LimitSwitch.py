from class_LimitSwitch_NiMax import LimitSwitch
import time


### -------- Limit Switches -------- ###
switch_xPlus_near = LimitSwitch("Dev1/port0/line24")
switch_xPlus_far = LimitSwitch("Dev1/port0/line25")

switch_xMinus_near = LimitSwitch("Dev1/port0/line26")
switch_xMinus_far = LimitSwitch("Dev1/port0/line27")

switch_yPlus_near = LimitSwitch("Dev1/port0/line28")
switch_yPlus_far = LimitSwitch("Dev1/port0/line29")

switch_yMinus_near = LimitSwitch("Dev1/port0/line30")
switch_yMinus_far = LimitSwitch("Dev1/port0/line31")


# Starting tasks
switch_xPlus_near.start_limit_switch()
switch_xPlus_far.start_limit_switch()

switch_xMinus_near.start_limit_switch()
switch_xMinus_far.start_limit_switch()

switch_yPlus_near.start_limit_switch()
switch_yPlus_far.start_limit_switch()

switch_yMinus_near.start_limit_switch()
switch_yMinus_far.start_limit_switch()


while True:
	value_xPlus_near = switch_xPlus_near.read_limit_switch()
    value_xPlus_far = switch_xPlus_far.read_limit_switch()
    
    value_xMinus_near = switch_xMinus_near.read_limit_switch()
    value_xMinus_far = switch_xMinus_far.read_limit_switch()
    
    value_yPlus_near = switch_yPlus_near.read_limit_switch()
    value_yPlus_far = switch_yPlus_far.read_limit_switch()
    
    value_yMinus_near = switch_yMinus_near.read_limit_switch()
    value_yMinus_far = switch_yMinus_far.read_limit_switch()
    
    print("xPlus_near: ", value_xPlus_near, "xPlus_far: ", value_xPlus_far, "xMinus_near: ", value_xMinus_near, "xMinus_far: ", value_xMinus_far,
        "yPlus_near:", value_yPlus_near, "yPlus_far: ", value_yPlus_far, "yMinus_near: ", value_yMinus_near, "yMinus_far: ", value_yMinus_far)
        
    time.sleep(0.01)  # Delay of 10 milliseconds
    