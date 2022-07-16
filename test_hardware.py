# hardware test script
from BobaHardware import BobaMachine


def test_flipper_basket(bob4):
	bob4.cook_tapioca()


def test_pumps(bob4):
	bob4.


def test_motors(bob4):
	for _ in range(2):
    	bob4.BobaFlipper.move(-6)
    	time.sleep(2)
    	bob4.BobaFlipper.move(6)
    	time.sleep(2)
	print("DONE")


def main():
	bob4 = BobaMachine()
	bob4.test_motors()
	bob4.ser.close()


if __name__ == '__main__':
	main()