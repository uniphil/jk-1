from .reel import Reel
import time

REEL_CMD = 0x11  # DC1
FRAME_CMD = 0x12  # DC2
CAM_SELECT = '*'
K103_SELECT = 'F'
K103_SELECT_R = 'R'


def init(device, description=None):
    description = description or '{} reel'.format(
        'Camera' if device == 'C' else 'Projector')
    return bytearray([
        REEL_CMD,
        '!',
        device,
    ]) + Reel(int(time.time()), description, 100, 1).to_bytes()


def get_reel(device):
    return bytearray([
        REEL_CMD,
        '?',
        device,
    ])


def get_frame(device):
    return bytearray([
        FRAME_CMD,
        '?',
        device,
    ])


def update_reel(device, reel):
    return bytearray([
        REEL_CMD,
        '!',
        device,
    ]) + reel.to_bytes()


def advance(device, n):
    return bytearray([
        FRAME_CMD,
        '!',
        device,
    ]) + Reel.pack_advance_number(n)


def cancel_advances():
    return bytearray([FRAME_CMD, 'x'])


def dump(what):
    return bytearray(['_', what])
