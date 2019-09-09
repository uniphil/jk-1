#!/usr/bin/env python

from serial import Serial
from serial.threaded import ReaderThread
from serial.tools import list_ports
from Tkinter import Tk
import traceback
import tkMessageBox
from charlie_app import ui
from packetizer import Packetizer


HELP = """\
Charlie controller

Usage: {} [PORT]

PORT - serial port for arduino (should auto-detect)
"""


def show_error(self, *args):
    err = traceback.format_exception(*args)
    tkMessageBox.showerror('Exception', err)
    raise


Tk.report_callback_exception = show_error


if __name__ == '__main__':
    import sys
    try:
        port = sys.argv[1]
    except IndexError:
        maybes = list(list_ports.grep('usb'))
        if len(maybes) == 0:
            tkMessageBox.showerror('Not connected', 'Cannot find USB device')
            sys.stderr.write(
                'missing serial port (maybe /dev/tty.usbserial-something)\n')
            sys.exit(1)
        if len(maybes) > 1:
            sys.stderr.write(
                'not sure which serial port to use. '
                'likely candidates:\n{}\n'.format(
                    '\n'.join(map(lambda m: '{}\t{}\t{}'.format(
                        m.device, m.description, m.manufacturer), maybes))))
            sys.exit(1)
        port = maybes[0].device

    s = Serial(port, 9600)

    with ReaderThread(s, Packetizer) as device:
        app = ui.App(device=device)
        app.master.lift()  # dunno why this helps with first render
        app.mainloop()
