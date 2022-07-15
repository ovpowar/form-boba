import serial
import time

# ---- KEY
# rice cooker = R
# latch = L
# boba dispense (BF) = A
# tea = B
# raw boba dispense (RBD) = C
# shot dispenser 1 = X
# shot dispenser 2 = Y
# simple syrup = Z

stepper_conversion = 1.8 # degrees per step
cooking_time = 4 # minutes for boba cooking
transfer_time = 5 # seconds wait after flipping the basket


class Comms():
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyUSB0', 115200)
	
	def send_comm(self,comm,msg):
		msg = msg+'\n'
		msg2 = bytes(msg, 'utf-8')
		print(msg2)
		response = comm.ser.write(msg2)
		print(response)
		comm.ser.flush()
		# self.ser.reset_input_buffer()

class GeneralObject():
	def __init__(self,objID,obj_type,speed,accel):
		self.objID = objID
		self.obj_type = obj_type
		self.speed = speed
		self.accel = accel

	def turn_on(self,comm): # for latches and actuators only
		if self.obj_type == 'actuator':
			comm.send_comm('B1'+ str(self.objID)+' 1')
		else:
			print('Cannot turn on this object- this object is not an actuator')

	def turn_off(self,comm): # for latches and actuators only
		if self.obj_type == 'actuator':
			comm.send_comm(f'B1 {self.objID} 0')
		else:
			print('Cannot turn on this object- this object is not an actuator')

	def move_motor(self,comm,accel,speed,revs):
		if self.obj_type == 'stepper':
			time.sleep(1)
			comm.send_comm(comm,"B92 "+str(self.objID)+" "+str(accel)) # set speed in mm/s2
			time.sleep(1)
			comm.send_comm(comm,"B91 "+str(self.objID)+" "+str(speed)) # set speed in mm/s
			time.sleep(5)
			comm.send_comm(comm,"B0 "+str(self.objID)+" "+str(revs)) #stepper move in rev
		else:
			print('Cannot move this object- this object is not an stepper')

	def run_pump(self,comm,accel,speed,revs):
		if self.obj_type == 'pump':
			comm.send_comm(f'B92 {self.objID} {accel}') # set speed in mm/s2
			comm.send_comm(f'B91 {self.objID} {speed}') # set speed in mm/s
			comm.send_comm(f'B0 {self.objID} {revs}') #stepper move in rev
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
	    self.R = GeneralObject('R','actuator',0,0)
	    self.L = GeneralObject('L','actuator',0,0)
	    self.A = GeneralObject('A','stepper',0.5,40000)
	    self.B = GeneralObject('B','pump',0.5,40000)
	    self.C = GeneralObject('C','stepper',0.5,40000)
	    self.X = GeneralObject('X','pump',0.5,40000)
	    self.Y = GeneralObject('Y','pump',0.5,40000)
	    self.Z = GeneralObject('Z','pump',0.5,40000)
	    self.order_queue = OrderQueue()
	    self.flavors = {}
	    self.status = "Ready"
	    self.update_flavors("PassionFruit", "Mango")
	    self.comm = Comms()

	
	def test_code(self):
	    print("HELLO")
	    # self.L.turn_on()
	    self.C.move_motor(self.comm,120000,40000,-7)
	    # test_list = [self.A, self.B, self.C, self.X, self.Y, self.Z]
	    # actuator_list = [self.L, self.R]
	    # msg0 = input('M (motor) or A (actuator)? ')
	    # if msg0 == 'M':
		   #  i = input('Choose device? 0-5 for ABCXYZ ')
		   #  msg1 = input('Accel in mmps2: ')
		   #  msg2 = input('Speed in rev/s: ')
		   #  msg3 = input('Num revs: ')
		   #  test_list[int(i)].move_motor(int(msg1), int(msg2), int(msg3))
	    # if msg0 == 'A':
		   #  msg0 = input('Choose device? 0-1 for LR ')
		   #  test_list[int(i)].turn_on()
		   #  time.sleep(5)
		   #  test_list[intt(i)].turn_off()

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
		self.make_boba(self, self.order_queue.d[order])
		self.order_queue.q[order]["status"] = "Finished"

	def update(self, order_queue):
		self.order_queue = order_queue
		print(order_queue)

	def cook_tapioca(self):
		self.transfer_boba() # lifts the lid
		dispense_angle = 95
		steps = dispense_angle / stepper_conversion
		response = self.C.move_motor(self.C.accel,self.C.speed,steps) # dispense the boba into the rice cooker
		self.R.turn_on() # turn on the rice cooker
		time.sleep(cooking_time*60) # cooking the boba time
		self.R.turn_off() # turn of the rice cooker
		self.transfer_boba()
		self.release_latch()

	def transfer_boba(self):
		transfer_angle = 180
		steps = dispense_angle / stepper_conversion
		response = self.A.move_motor(self.A.accel,self.A.speed,steps) # dump out the boba
		time.sleep(transfer_time)
		response = self.A.move_motor(self.A.accel,self.A.speed,-steps) # return the basket

	def release_latch(self):
		response = self.L.turn_off()

	def dispense_tea():
		tea_volume = 250 #mL
		dose = 15 #mL/rev
		revs = tea_volume/dose
		self.B.run_pump(self.B.accel, self.B.speed,revs)

	def dispense_syrup(syrup_level):
		syrup_factor = 2 #100% / 50mL
		dose = 15 #mL/rev
		revs = syrup_factor/syrup_level/dose
		self.Z.run_pump(self.Z.accel,self.Z.speed,revs)

	def dispense_flavors(flavor,which_pump):
		flavor_vol = 15 #mL
		dose = 15 #mL/rev
		revs = flavor_vol/dose
		which_pump.run_pump(self.which_pump.accel,self.which_pump.speed,revs)

	def make_boba(self, current_order):
		if current_order['is_tapioca']:
			self.cook_tapioca()
		if current_order['is_shot1']: 
			self.dispense_flavors(self.flavors['shot1'], self.X)
		if current_order['is_shot2']:
			self.dispense_flavors(self.flavors['shot2'], self.Y)
		self.dispense_syrup(syrup_level)
		self.dispense_tea()



if __name__ == "__main__":
	bob4 = BobaMachine()
	bob4.test_code()

	


