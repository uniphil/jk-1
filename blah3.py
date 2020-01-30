from packet_serial import Packetizer
from serial import Serial
from serial.tools import list_ports
from serial.threaded import ReaderThread
from time import mktime, sleep
from charlie_app import k103
from charlie_app.reel import Reel


REEL_CMD = 0x11  # DC1
FRAME_CMD = 0x12  # DC2
CAM_SELECT = '*'
K103_SELECT = 'F'
K103_SELECT_R = 'R'


def handle_packet(bs):
    stuff = iter(bs)
    target = stuff.next()
    if target == REEL_CMD:
        cmd = stuff.next()
        if cmd == ord('i'):
            print '{} reel'.format(chr(stuff.next()))
            reel_bytes = bytearray(stuff)
            try:
                reel = Reel.from_bytes(reel_bytes)
            except AssertionError as e:
                print 'nah', e
                print ' '.join('{:02X}'.format(b) for b in reel_bytes)
            else:
                print reel
        else:
            raise NotImplementedError(
                'reel command (0x{0:02X} {0:d} {0:c}) not there yet'.format(
                    cmd))
    elif target == FRAME_CMD:
        cmd = stuff.next()
        if cmd == ord('i'):
            print '{:c} frame: {}'.format(
                stuff.next(), Reel.frame_from_bytes(bytearray(stuff)))
        else:
            raise NotImplementedError(
                'frame command (0x{0:02X} {0:d} {0:c}) not there yet'.format(
                    cmd))
    else:
        print 'woo got packet:'
        print '\n'.join('  0x{0:02X}  {0:3d}  {0:c}'.format(b) for b in bs)


if __name__ == '__main__':
    import sys
    try:
        port = sys.argv[1]
    except IndexError:
        maybes = list(list_ports.grep('usb'))
        if len(maybes) == 0:
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

    with ReaderThread(s, Packetizer(handle_packet)) as device:
        sleep(2)
        # reel = Reel(
        #     mktime((2019, 05, 16, 0, 0, 0, 0, 0, -1)),
        #     'asdfasdfasdf',
        #     100, 50)
        # device.send(k103.update_reel('P', reel))
        device.send(k103.advance('P', 5))
        # while True:
        #     # device.send(k103.get_frame('C'))
        #     # device.send(k103.get_frame('P'))
        #     # device.send(k103.get_reel('C'))
        #     # device.send(k103.get_reel('P'))
        #     sleep(2)
        #     # device.send('.')

    sleep(0.5)

    # pprint(['0x{0:02X}  {0:3d}  {0:c}'.format(ord(c)) for c in t])

    s.close()
