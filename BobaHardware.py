import pyserial

actuators = ['R', 'L']
steppers = ['A', 'B', 'C', 'X', 'Y', 'Z']

class GeneralObject(ser,objID):
	def __init__(self):
		self.objID = objID


	def send_comm(self, msg):
		ser.write(b'{msg}')
		# some encoding / decoding
		try: # something like this??
			response = ser.readline()
		except:
			print('?')
		finally:
			print(response)


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
	    ser = serial.Serial('dev/ttyUSB',
                    baudrate=9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE)
	    ser.port = 'COM4'
	    # TESTING ONLY
	    ser.write(b'L1')
	    response = ser.readline()
	    print(response)


	def update(self, order_queue):
		print(order_queue)
			
	def main(self,...):
		#turn on rice cooker



