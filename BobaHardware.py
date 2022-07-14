import serial

actuators = ['R', 'L']
steppers = ['A', 'B', 'C', 'X', 'Y', 'Z']

class GeneralObject():
	def __init__(self,objID):
		self.objID = objID

	def send_comm(self, msg):
		command = self.ser.write(msg.encode())
		# some encoding / decoding
		try: # something like this??
			#response = ser.readline()
			line = ser.readline().decode('utf-8').rstrip()
		except:
			print('?')
		finally:
			print(line)
			ser.reset_input_buffer()

	def turn_on(objID): # for latches and actuators only
		if objID in actuator:
			send_comm(f'{objID}1')
		else:
			print('Cannot turn on this object- this object is not an actuator')

	def turn_off(objID): # for latches and actuators only
		if objID in actuators:
			send_comm(f'{objID}0')
		else:
			print('Cannot turn on this object- this object is not an actuator')


	def move_motor(objID,step):
		if objID in steppers:
			send_comm(f'{objID}{step}')


class BobaMachine():
	def __init__(self):
	    self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
	    # ser = serial.Serial('dev/ttyUSB',
     #                baudrate=9600,
					# parity=serial.PARITY_NONE,
					# stopbits=serial.STOPBITS_ONE)
	    #ser.port = 'COM4'
	    # TESTING ONLY
	
	def test_code(self):
	    msg = input('Message? ')
	    command = self.ser.write(msg.encode())
	    line = self.ser.readline().decode('utf-8').rstrip()
	    print(command, line)


	def update(self, order_queue):
		print(order_queue)
			
	#def main(self,...):
		#turn on rice cooker

if __name__ == "__main__":
	bob4 = BobaMachine()
	bob4.test_code()

