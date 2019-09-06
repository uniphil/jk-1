BYTE_DEBUG_FMT = '  0x{0:02X}  {0:3d}  {0:c}'

out = []


def hs(s):
    return ' '.join('{:02X}'.format(d) for d in s)


def p1(b, msg=None):
    out.append((b, msg))


def pl(bs, length, msg=None):
    assert length <= len(bs)
    out.extend((b, msg) for b in bs[:length])


def get_sequence_length(stuff, bytes_left):
    i = 0
    while i < bytes_left:
        byte = 0x00 if i + 1 == bytes_left else stuff[i]
        if byte == 0x00:
            i += 1
            break
        i += 1
    return i


def send(stuff, length):
    length = length + 1
    p1(0x00, 'packet start')
    p1(length, 'packet len')

    sequence_start = 0
    while True:
        bytes_left = length - sequence_start
        sequence_length = get_sequence_length(
            stuff[sequence_start:], bytes_left)
        p1(sequence_length, 'seq len')
        pl(stuff[sequence_start:], sequence_length - 1, 'seq')
        sequence_start += sequence_length
        if sequence_start >= length:
            break


def unstuff(data, out_length):
    seq_length = 0
    i = 0
    while i < out_length:
        seq_length = data[i]
        while seq_length > 1:
            data[i] = data[i+1]
            i += 1
            seq_length -= 1
        data[i] = 0x00
        i += 1


def rx(packet):
    started = False
    next_byte = 0x00
    out_length = 0
    out_index = 0
    get = iter(packet)
    rx_out = bytearray([0x00] * 62)
    while out_length == 0 or out_index < out_length:
        next_byte = get.next()
        if next_byte == 0x00:
            assert not started
            out_length = 0
            out_index = 0
            started = True
            continue
        assert started
        if out_length == 0:
            out_length = next_byte
            continue
        rx_out[out_index] = next_byte
        out_index += 1
    out_length -= 1
    unstuff(rx_out, out_length)
    return rx_out[:out_length]


def s(data, expected):
    global out
    out = []
    send(data, len(data))
    out_simple = list(a for a, _ in out)
    if (not all(a == b for a, b in zip(out_simple, expected)) or
       len(out) != len(expected)):
        print '\nerr:\t\t\t  ', hs(data)
        print '\texpected:', hs(expected)
        print '\t   found:', hs(a for a, _ in out)
        for b, m in out:
            print '\t{}\t{}'.format(BYTE_DEBUG_FMT.format(b), m)
    cobs = out_simple[2:]
    unstuffed = list(cobs)
    unstuff(unstuffed, len(cobs))
    unstuffed = unstuffed[:-1]
    if (not all(a == b for a, b in zip(data, unstuffed)) or
       len(data) != len(unstuffed)):
        print '\nerr:\t     ', hs(data)
        print '\tcobs:', hs(cobs)
        print '\tunst:', hs(unstuffed)

    rxed = rx(out_simple)
    if (not all(a == b for a, b in zip(data, rxed)) or
       len(data) != len(rxed)):
        print 'errrrrr', hs(data)


if __name__ == '__main__':
    s([0x00], [0x00, 0x02, 0x01, 0x01])
    s([0xFF], [0x00, 0x02, 0x02, 0xFF])
    s([0x00, 0x00], [0x00, 0x03, 0x01, 0x01, 0x01])
    s([0x00, 0xFF], [0x00, 0x03, 0x01, 0x02, 0xFF])
    s([0xFF, 0x00], [0x00, 0x03, 0x02, 0xFF, 0x01])
    s([0xFF, 0xFF], [0x00, 0x03, 0x03, 0xFF, 0xFF])
    s([0x00, 0x00, 0x00], [0x00, 0x04, 0x01, 0x01, 0x01, 0x01])
    s([0xFF, 0x00, 0x00], [0x00, 0x04, 0x02, 0xFF, 0x01, 0x01])
    s([0x00, 0xFF, 0x00], [0x00, 0x04, 0x01, 0x02, 0xFF, 0x01])
    s([0x00, 0x00, 0xFF], [0x00, 0x04, 0x01, 0x01, 0x02, 0xFF])
    s([0xFF, 0x00, 0xFF], [0x00, 0x04, 0x02, 0xFF, 0x02, 0xFF])
    s([0xFF, 0xFF, 0xFF], [0x00, 0x04, 0x04, 0xFF, 0xFF, 0xFF])
