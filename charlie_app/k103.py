from time import sleep
from .reel import Reel

REEL_CMD = 0x11  # DC1
FRAME_CMD = 0x12  # DC2
CAM_SELECT = '*'
K103_SELECT = 'F'
K103_SELECT_R = 'R'


def capture(s, device, n):
    s.write(bytearray([FRAME_CMD, device, n]))


def get_reel(s, device):
    buffer_trash = s.read(s.in_waiting)
    print 'cleared buffer before command:', buffer_trash
    s.write(bytearray([
        REEL_CMD,
        '?',
        device,
    ]))
    print 'sent command. waiting for reel...'
    sleep(1)
    print '(any time now...)'
    bytes = s.read(32)
    print 'got reel!'
    return Reel.from_bytes(bytes)
