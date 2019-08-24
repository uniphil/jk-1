#!/usr/bin/env python

from charlie_app import ui


HELP = """\
Charlie controller

Usage: {} [PORT]

PORT - serial port for arduino (should auto-detect)
"""


if __name__ == '__main__':
    import sys
    try:
        serial_port = sys.argv[1]
    except IndexError:
        serial_port = None

    app = ui.App(serial_port=serial_port)
    app.master.lift()  # dunno why this helps with first render
    app.mainloop()
