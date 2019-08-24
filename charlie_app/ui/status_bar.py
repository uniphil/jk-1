import Tkinter as tk
import ttk
from serial.tools import list_ports


class StatusBar(ttk.Frame):
    def __init__(self, master, connect):
        ttk.Frame.__init__(self, master)
        self.connect=connect

        # maybes = list(list_ports.grep('usb'))
        # if len(maybes) == 0:
        #     sys.stderr.write(HELP.format(sys.argv[0]))
        #     sys.stderr.write('\nError: missing serial port (probably /dev/tty.usbserial-something)\n')
        #     sys.exit(1)
        # if len(maybes) > 1:
        #     sys.stderr.write('not sure which serial port to use. likely candidates:\n{}\n'.format(
        #         '\n'.join(map(lambda m: '{}\t{}\t{}'.format(m.device, m.description, m.manufacturer), maybes))))
        #     sys.exit(1)
        # port = maybes[0].device

        # s = Serial(port, 9600)

        # time.sleep(1)
        # t = s.read(s.in_waiting)
        # print(t)
