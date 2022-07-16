import serial
import time
from enum import Enum

# ---- KEY
# rice cooker = R
# latch = L
# boba dispense (BF) = A
# tea = B
# raw boba dispense (RBD) = C
# shot dispenser 1 = X
# shot dispenser 2 = Y
# simple syrup = Z

def calculate_dose(volume):
    flow_rate_mLps = 15
    speed_rps = 1000 # follow pump speed
    revs = volume/flow_rate_mLps*speed_rps
    return revs

class Comms:
    def __init__(self):
        self.ser = serial.Serial('/dev/tty.usbserial-0001', 115200)
        time.sleep(1) # for luck
    
    def send_comm(self,msg):
        msgg = bytes(msg + '\n', 'utf-8')
        print(msgg)
        self.ser.write(msgg)
        print(self.ser.readline())
        self.ser.flush()

class Stepper:
    def __init__(self, comm, speed, acceleration, bCodeID):
        self.comm = comm
        self.speed = speed
        self.acceleration = acceleration
        self.id = bCodeID
        self._init_motor_settings()

    def _init_motor_settings(self):
        # set acceleration
        self.comm.send_comm("B92 {} {}".format(self.id, self.acceleration))
        time.sleep(1)
        self.comm.send_comm("B91 {} {}".format(self.id, self.speed))
        time.sleep(1)

    def move(self, revs):
        self.comm.send_comm("B0 {} {}".format(self.id, revs))

class Relay:
    def __init__(self, comm, bCodeID):
        self.comm = comm
        self.id = bCodeID

    def set_active(self, isActive):
        self.comm.send_comm("B1 {} {}".format(self.id, str(1) if isActive else str(0)))



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
        ser = Comms()

        # Initialize Steppers
        dispenser_speed = 1500
        dispenser_acceleration = 1000
        flipper_speed = 500
        flipper_acceleration = 300
        pump_speed = 10
        pump_acceleration = 30
        self.RawBobaDispenser = Stepper(ser, dispenser_speed, dispenser_acceleration, 'B')
        self.BobaFlipper = Stepper(ser, flipper_speed, flipper_acceleration, 'C')
        self.ShotDispense1 = Stepper(ser, pump_speed, pump_acceleration, 'X')
        self.ShotDispense2 = Stepper(ser, pump_speed, pump_acceleration, 'Y')
        self.ShotDispense3 = Stepper(ser, pump_speed, pump_acceleration, 'Z')
        self.ShotDispense4 = Stepper(ser, pump_speed, pump_acceleration, 'A')

        # Initialize Relays
        self.Latch = Relay(ser, 'L')
        self.RiceCooker = Relay(ser, 'R')

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
        self.make_boba(self, self.order_queue.d[order])
        
    def update(self, order_queue):
        self.order_queue = order_queue
        print(order_queue)

    def cook_tapioca(self):
        self.lift_lid(15) # lifts the lid
        self.return_strainer(15) # strainer comes back
        self.dispense_raw_boba() # dispenses through the hopper
        self.drop_lid()
        time.sleep(400)
        self.lift_lid(15)  # lifts the lid

    def lift_lid(self, revolutions):
        # revolutions = transfer_angle/360
        self.Latch.set_active(True)
        time.sleep(1)
        self.BobaFlipper.move(revolutions)
        time.sleep(10)

    def return_strainer(self, revolutions):
        # revolutions = transfer_angle/360
        self.BobaFlipper.move(-revolutions)
        time.sleep(10)

    def dispense_raw_boba(self, dispense_revolutions):
        self.RawBobaDispenser.move(dispense_revolutions)
        time.sleep(abs(1*dispense_revolutions))

    def drop_lid(self):
        self.Latch.set_active(False)
        time.sleep(1)

    def calculate_dose(tea_volume):
        dose = 1.5 # mL/rev
        return tea_volume/dose

    def dispense_tea(room_for_milk):
        tea_volume = 250 # mL
        revolutions = calculate_dose(tea_volume)
        revolutions = revolutions/2 if room_for_milk else revolutions
        self.ShotDispense4.move(revolutions)
        time.sleep(abs(2*revolutions))

    def dispense_syrup(syrup_level):
        Max_mL = 30 # mL = 2 tbsp
        syrup_vol = syrup_level/100*Max_mL
        revolutions = calculate_dose(syrup_vol)
        self.ShotDispense3.move(revolutions)
        time.sleep(abs(revolutions*2))

    def dispense_flavors(ShotDispense):
        flavor_vol = 3 #mL
        revolutions = calculate_dose(flavor_vol)
        ShotDispense.move(revolutions)
        time.sleep(1*revolutions)


    def make_boba(self, current_order):
        if current_order['is_tapioca']:
            self.cook_tapioca()
        if current_order['is_shot1']: 
            self.dispense_flavors(self.ShotDispense1)
        if current_order['is_shot2']:
            self.dispense_flavors(self.ShotDispense2)
        self.dispense_syrup(syrup_level)
        room_for_milk = current_order['room_for_milk']
        self.dispense_tea(room_for_milk)
    
if __name__ == "__main__":
    bob4 = BobaMachine()

    
