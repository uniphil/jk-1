import logging
from serial.threaded import Protocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('packetizer')


PACKET_NORMAL = 0b00 << 6
PACKET_RX_ERR = 0b01 << 6
PACKET_TX_ERR = 0b10 << 6
PACKET_USER_LOG = 0b11 << 6


BYTE_DEBUG_FMT = '  0x{0:02X}  {0:3d}  {0:c}'


def stuff(data):
    out = bytearray()
    for part in data.split(chr(0x00)):
        out.extend(chr(len(part) + 1) + part)
    return out


def unstuff(stuffed):
    out = bytearray()
    bytes = iter(stuffed)
    for count in bytes:
        for _ in range(count - 1):
            out.append(bytes.next())
        out.append(0x00)
    return out[:-1]


def Packetizer(handle_packet):
    def instantiate(*args, **kwargs):
        instance = _Packetizer(*args, **kwargs)
        setattr(instance, 'handle_packet', handle_packet)
        return instance
    return instantiate


class _Packetizer(Protocol):
    def __init__(self):
        self.transport = None
        self.packet_started = False
        self.packet_bytes_remaining = None
        self.packet_mode = PACKET_NORMAL
        self.contents = bytearray()

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        self.transport = None
        super(_Packetizer, self).connection_lost(exc)

    def data_received(self, data):
        byte_data = bytearray(data)

        if self.packet_started is False and 0x00 not in byte_data:
            return self.handle_unexpected_bytes(byte_data)

        for byte in byte_data:
            logger.debug(
                'rx byte {}'.format(BYTE_DEBUG_FMT.format(byte)))
            if byte == 0x00:
                if self.packet_started:
                    self.handle_incomplete(self.contents)
                self.contents = bytearray()
                self.packet_bytes_remaining = None
                self.packet_started = True
                continue

            if self.packet_started is False:
                self.handle_unexpected_bytes(bytearray([byte]))
                continue

            elif self.packet_bytes_remaining is None:
                self.packet_mode = byte & (0xFF << 6)
                self.packet_bytes_remaining = byte & (0xFF >> 2)
                continue

            self.contents.append(byte)
            self.packet_bytes_remaining -= 1

            if self.packet_bytes_remaining > 0:
                continue

            self.handle_stuffed_packet(self.contents, self.packet_mode)
            self.packet_started = False
            self.packet_bytes_remaining = None
            self.contents = bytearray()

    def handle_stuffed_packet(self, bytes, packet_mode):
        try:
            unstuffed = unstuff(bytes)
        except Exception as e:
            self.handle_unstuff_error(e)
        else:
            if packet_mode == PACKET_NORMAL:
                self.handle_packet(unstuffed)
            else:
                self.handle_alt_mode_packet(unstuffed, packet_mode)

    def handle_unstuff_error(self, error):
        logger.error('Could not unstuff packet:\n{}'.format(
            '\n'.join(BYTE_DEBUG_FMT.format(b) for b in bytes)))

    def handle_packet(self, bytes):
        raise NotImplementedError('implement handle_packet to use stuff')

    def handle_alt_mode_packet(self, data, mode):
        if mode == PACKET_RX_ERR:
            logger.error('RX error packet: {!r}'.format(bytes(data)))
        elif mode == PACKET_TX_ERR:
            logger.error('TX error packet: {!r}'.format(bytes(data)))
        elif mode == PACKET_USER_LOG:
            logger.info('log: {!r}'.format(bytes(data)))

    def handle_incomplete(self, bytes):
        logger.error('Incomplete packet. Garbage:\n{}'.format(
            '\n'.join(BYTE_DEBUG_FMT.format(b) for b in bytes)))

    def handle_unexpected_bytes(self, data):
        logger.error('Unexpected bytes before packet: {!r}'.format(
            bytes(data)))

    def send(self, data, mode=PACKET_NORMAL):
        logger.debug('sending data:\n{}'.format(data))

        assert len(data) <= 62, \
            'data must be 62 bytes or less to stuff, found {} bytes'.format(
                len(data))
        body = stuff(data)
        header = bytearray([0x00, len(body) | mode])
        assert len(body) == len(data) + 1
        packet = header + body
        assert len(packet) <= 64, \
            'encoding: packet of length {} should have been <= 64'.format(
                len(packet))

        logger.debug('(as packet:)\n{}'.format(
            '\n'.join(BYTE_DEBUG_FMT.format(d) for d in packet)))

        return self.transport.write(packet)
