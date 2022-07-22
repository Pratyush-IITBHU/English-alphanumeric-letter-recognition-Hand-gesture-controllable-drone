from pyfirmata import Arduino, util
import time


class Controller:

    def __init__(self):
        self.board = Arduino('COM3')                        # Select Arduino Port
        self.signalPin_x = self.board.get_pin('d:3:p')      # DigitalPin 3
        self.signalPin_y = self.board.get_pin('d:5:p')      # DigitalPin 5
        self.signalPin_z = self.board.get_pin('d:6:p')      # DigitalPin 6

    def analog_out(self, val_x, val_y, val_z):

        self.signalPin_x.write(val_x)
        time.sleep(0.05)

        self.signalPin_y.write(val_y)
        time.sleep(0.05)

        self.signalPin_z.write(val_z)
        time.sleep(0.05)

    def close(self):
        self.board.exit()


