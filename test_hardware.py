# hardware test script
from BobaHardware import BobaMachine


def test_flipper_basket(bob4):
	bob4.cook_tapioca()


def test_tea(bob4):
	bob4.dispense_tea()


def test_syrup(bob4,syrup_level):
	bob4.dispense_syrup(syrup_level)

def test_flavors(bob4):
	bob4.dispense_flavors(bob4.ShotDispense1)
	bob4.dispense_flavors(bob4.ShotDispense2)


def test_motors(bob4):
	for _ in range(2):
    	bob4.BobaFlipper.move(-6)
    	time.sleep(2)
    	bob4.BobaFlipper.move(6)
    	time.sleep(2)
	print("DONE")

	
if __name__ == '__main__':
	bob4 = BobaMachine()