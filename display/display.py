__author__ = 'faebser'


class LcdDisplay(object):
    try:
        import Adafruit_CharLCD
        display = Adafruit_CharLCD.Adafruit_CharLCDPlate()
    except Exception, e:
        print('No LCD Display available')
        display = None

    def set_color(self, r, g, b):
        if self.display is not None:
            self.display.set_color(r, g, b)
        else:
            pass

    def clear(self):
        if self.display is not None:
            self.display.clear()
        else:
            pass

    def info(self, info):
        self.set_color(1.0, 1.0, 0)
        self.message(info)

    def error(self, error):
        self.set_color(1.0, 0, 0)
        self.message(error)

    def message(self, message):
        if self.display is not None:
            self.display.clear()
            self.display.message(message)
        else:
            print(message)
