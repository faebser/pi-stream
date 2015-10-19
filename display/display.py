from multiprocessing import Process, Queue, Lock
from time import sleep
__author__ = 'faebser'

# mutex
mutex = Lock()


def lcd_thread(display, lcd_queue, reset_queue):
    messages_list = []
    index = 0
    while True:
        sleep(5)
        print('i slept for 5 second')
        if reset_queue.empty() != True:
            print(reset_queue.get_nowait())
            messages_list = []
        if lcd_queue.empty() != True:
            messages_list.append(lcd_queue.get_nowait())
        if len(messages_list) != 0:
            display.message(messages_list[index])
            index = index + 1
            if index == len(messages_list):
                index = 0


class LcdDisplay(object):

    def __init__(self, lcd_queue):
        try:
            import Adafruit_CharLCD
            self.display = Adafruit_CharLCD.Adafruit_CharLCDPlate()
            self.reset_queue = Queue()
            process = Process(target=lcd_thread, args=(self, lcd_queue, self.reset_queue))
            process.start()
        except Exception, e:
            print('No LCD Display available')
            self.reset_queue = Queue()
            self.display = None
            process = Process(target=lcd_thread, args=(self, lcd_queue, self.reset_queue))
            process.start()

    def reset(self):
        self.reset_queue.put('reset')

    def set_color(self, r, g, b):
        if self.display is not None:
            with mutex:
                self.display.set_color(r, g, b)
        else:
            pass

    def clear(self):
        if self.display is not None:
            with mutex:
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
            with mutex:
                self.display.clear()
                self.display.message(message)
        else:
            print(message)
