import serial

# ---- KEY
# rice cooker = R
# latch = L
# boba dispense = A
# tea = B
# raw boba dispense = C
# shot dispenser 1 = X
# shot dispenser 2 = Y
# simple syrup = Z

actuators = ['R', 'L']
steppers = ['A', 'B', 'C']
pumps = ['X', 'Y', 'Z']

stepper_conversion = 1.8 # degrees per step
cooking_time = 4 # minutes for boba cooking
transfer_time = 5 # seconds wait after flipping the basket


class GeneralObject():
	def __init__(self,objID):
		self.objID = objID

	def send_comm(self, msg):
		response = self.ser.write(msg.encode())
		ser.reset_input_buffer()
		print(msg, response)
		return response


	def turn_on(objID): # for latches and actuators only
		if objID in actuators:
			send_comm(f'{objID}1')
		else:
			print('Cannot turn on this object- this object is not an actuator')

	def turn_off(objID): # for latches and actuators only
		if objID in actuators:
			send_comm(f'{objID}0')
		else:
			print('Cannot turn on this object- this object is not an actuator')

	def move_motor(objID,accel):
		if objID in steppers:
			send_comm(f'{objID}91 {accel}')
		else:
			print('Cannot move this object- this object is not an motor')

	def run_pump(objID,speed):
		if objID in pumps:
			send_comm(f'{objID} {speed}')
		else:
			print('Cannot run this object- this object is not a pump')


class OrderQueue():
	def __init__(self):
		self.q = []

	def update(self, order):
		self.q.append(order)

	def update_sequence(self):
		k = 0
		for i in self.q:
			k +=1
			i['queue_number'] = k

	def remove_order_number(self, number):
		self.q.pop(number-1)
		self.update_sequence()

class BobaMachine():
	def __init__(self):
	    # self.ser = serial.Serial('/dev/tty.usbserial-0001', 115200)
	    self.R = GeneralObject('R')
	    self.L = GeneralObject('L')
	    self.A = GeneralObject('A')
	    self.B = GeneralObject('B')
	    self.C = GeneralObject('C')
	    self.X = GeneralObject('X')
	    self.Y = GeneralObject('Y')
	    self.Z = GeneralObject('Z')
	    self.order_queue = OrderQueue()
	    self.flavors = {}
	    self.status = "Ready"
	    self.update_flavors("PassionFruit", "Mango")
	
	def update_flavors(self, f1, f2):
		if f1 is not None:
			self.flavors['shot1'] = f1
		if f2 is not None:
			self.flavors['shot2'] = f2

	def check_order(self, number):
		if self.order_queue.q[number - 1]["status"] == "Queued":
			if self.status == "Ready":
				return "Ready"
			else:
				return "Wait"

	def start_preparing_order(self, order):
		self.order_queue.q[order]["status"] = "Cooking"

	def test_code(self):
	    # msg = input('Message? ')
	    # print(msg, type(msg))
	    # self.ser.write(msg.encode())
	    print("HELLO")
	    self.C.move_motor(1)

	def update(self, order_queue):
		self.order_queue = order_queue
		print(order_queue)

	def initialize_boba(self):
		'''dispenses boba and starts rice cooker'''
		dispense_angle = 95
		steps = dispense_angle / stepper_conversion
		response = self.C.move_motor(step_size)
		self.R.turn_on()
	
	def transfer_boba(self):
		'''transfer the boba from ricee cooker to cup'''
		transfer_angle = 180
		steps = dispense_angle / stepper_conversion
		response = self.A.move_motor(step_size)
		time.sleep(transfer_time)
		response = self.A.move_motor(-step_size)

	def latch(self):
		'''release latch and lower lid'''
		latch_steps = 10 # what is this irl? steps up to release the latch
		latch_range_angle = 90 #deg range of motion of the latch
		steps = latch_range_angle / stepper_conversion
		response = self.A.turn_off()
		time.sleep(5)
		response = self.A.move_motor(steps)

	def dispense_liquids():
		'''dispense all the liquids and syrups'''
		pass


	def make_boba(self):
		self.initialize_boba() # dispense the boba
		time.sleep(cooking_time*60) # cooking the boba time
		self.transfer_boba() # move boba to the cup
		self.latch() # move the latch and lid
		self.dispense_liquids() # dispense all off the liquids


if __name__ == "__main__":
	bob4 = BobaMachine()
	bob4.test_code()
	# bob4.make_boba()


