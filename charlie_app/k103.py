from time import sleep

REEL_CMD = 0x11  # DC1
FRAME_CMD = 0x12  # DC2
CAM_SELECT = '*'
K103_SELECT = 'F'
K103_SELECT_R = 'R'

def capture(s, device, n):
    for frame in range(n):
        print(frame + 1)
        s.write(bytearray([FRAME_CMD, device, 1]))
        sleep(0.9 if device == CAM_SELECT else 1.3)

