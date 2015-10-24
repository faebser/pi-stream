from multiprocessing import Process, Queue, Lock
from time import sleep
__author__ = 'faebser'

# mutex
mutex = Lock()


def lcd_thread(display, lcd_queue, reset_queue):
    messages_list = []
    index = 0
    while True:
        while lcd_queue.empty() is False:
            messages_list.append(lcd_queue.get_nowait())
        sleep(4)
        if reset_queue.empty() is False:
            messages_list = []
        if len(messages_list) != 0:
            r, g, b = messages_list[index]['type']
            display.set_color(r, g, b)
            display.message(messages_list[index]['message'])
            index += 1
            if index == len(messages_list):
                index = 0


class LcdDisplay(object):

    def __init__(self):
        self.INFO = (1.0, 1.0, 0)
        self.ERROR = (1.0, 0, 0)
        self.GOOD = (0, 0.1, 0)

        try:
            import Adafruit_CharLCD
            self.display = Adafruit_CharLCD.Adafruit_CharLCDPlate()
            self.lcd_queue = Queue()
            self.reset_queue = Queue()

        except Exception, e:
            print('No LCD Display available')
            self.reset_queue = Queue()
            self.lcd_queue = Queue()
            self.display = None

    def start_process(self):
        process = Process(target=lcd_thread, args=(self, self.lcd_queue, self.reset_queue))
        process.start()

    def put(self, message, message_type=(0.1, 0.1, 1)):
        self.lcd_queue.put({'type': message_type, 'message': message})

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
