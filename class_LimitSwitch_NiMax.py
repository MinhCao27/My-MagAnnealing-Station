import nidaqmx

class LimitSwitch:
	def __init__(self, input_pin):
		self.input_pin = input_pin
        self.input_task = nidaqmx.Task()
        self.input_task.di_channels.add_di_chan(self.input_pin)
    
    def start_limit_switch(self):
        self.input_task.start()
    
    def read_limit_switch(self):
        value = self.input_task.read()
        return value # value=True means switch is connected, value=False means switch is not connected
        
    def stop_limit_switch(self):
        self.input_task.stop()
        self.input_task.close()
        