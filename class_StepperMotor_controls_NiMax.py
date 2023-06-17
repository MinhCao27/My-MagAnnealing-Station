import nidaqmx
from nidaqmx.constants import AcquisitionType
import time


class StepperMotor:
    def __init__(self, dir_pin, pul_pin, rev_count, pulse_count, low_duration, high_duration):
        self.dir_pin = dir_pin
        self.pul_pin = pul_pin
        self.rev_count = rev_count
        self.pulse_count = 200 * self.rev_count
        self.low_duration = low_duration
        self.high_duration = high_duration
        
        # self.running = False
        
        self.dir_task = nidaqmx.Task()
        self.pul_task = nidaqmx.Task()       
        self.dir_task.do_channels.add_do_chan(self.dir_pin)
        self.pul_task.co_channels.add_co_pulse_chan_time(self.pul_pin, low_time=self.low_duration, high_time=self.high_duration)
            
    def rotate_direction(self, direction):
        self.dir_task.write(direction)
        # self.pul_task.wait_until_done(timeout=-1)

    def start_motor(self):
        # self.running = True
    
        # self.pul_task.wait_until_done(timeout=10)
        if self.dir_task.is_task_done() and self.pul_task.is_task_done():
            print("Beginning task")

            self.pul_task.timing.cfg_implicit_timing(sample_mode=AcquisitionType.FINITE, samps_per_chan=10)

            self.dir_task.start()
            self.pul_task.start()
        else:
            print("Tasks are running")
        
        print("should task be done?")
        # self.running = False
        

    def stop_motor(self):
        # self.running = False
            
        self.dir_task.stop()
        self.pul_task.stop()
        self.dir_task.close()
        self.pul_task.close()
        