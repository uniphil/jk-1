import time
import Tkinter as tk
import ttk

from .reel_widgets import ReelInfo
from .program_widgets import Program
from .status_bar import StatusBar
from .. import k103
from ..reel import FRAME_CMD, REEL_CMD, Reel


class App(ttk.Frame):
    def __init__(self, device=None):
        t_init = time.time()
        ttk.Frame.__init__(self, None)
        self.device = device
        setattr(device, 'handle_packet', self.handle_packet)

        self.master.title('Charlie control')
        self.camera_reel = None
        self.camera_current_frame = tk.IntVar()
        self.camera_current_frame.set(0)
        self.camera_current_frame.trace('w', self.update_camera_frame)
        self.projector_reel = None
        self.projector_current_frame = tk.IntVar()
        self.projector_current_frame.set(0)
        self.projector_current_frame.trace('w', self.update_projector_frame)
        self.create_widgets()
        self.grid()

        dt = time.time() - t_init
        time.sleep(max(0, 2 - dt))
        self.device.send(k103.get_reel('C'))
        self.device.send(k103.get_reel('P'))

    def init_camera_reel(self, reel):
        self.camera_reel = reel
        self.camera_reel_widget = ReelInfo(
            self.camera_frame, 'camera', self.camera_reel,
            self.camera_current_frame, self.replace_camera_reel,
            self.handle_advance_frames)
        self.camera_reel_widget.grid(row=1, column=0)

    def init_projector_reel(self, reel):
        self.projector_reel = reel
        self.projector_reel_widget = ReelInfo(
            self.projector_frame, 'projector', self.projector_reel,
            self.projector_current_frame, self.replace_projector_reel,
            self.handle_advance_frames)
        self.projector_reel_widget.grid(row=1, column=0)

    def create_widgets(self):
        self.camera_frame = ttk.Frame(self)
        self.projector_frame = ttk.Frame(self)
        manual_frame = ttk.Frame(self)
        program_frame = ttk.Frame(self)
        status_bar_frame = ttk.Frame(self)

        camera_label = ttk.Label(self.camera_frame, text='Camera')
        self.camera_reel_widget = None

        projector_label = ttk.Label(self.projector_frame, text='Projector')
        self.projector_reel_widget = None

        self.program = Program(
            program_frame, self.camera_reel, self.projector_reel,
            self.run_program)

        # self.status_bar = StatusBar(
        #     status_bar_frame, self.connect_serial)

        self.camera_frame.grid(row=0, column=0)
        self.projector_frame.grid(row=0, column=1)
        manual_frame.grid(row=1, column=0, columnspan=2)
        program_frame.grid(row=2, column=0, columnspan=2)
        status_bar_frame.grid(row=3, column=0, columnspan=2)

        camera_label.grid(row=0, column=0)
        projector_label.grid(row=0, column=0)

        self.program.grid()

        d = ttk.Button(
            self, text='Dump',
            command=lambda: self.device.send(k103.dump('T')))
        d.grid()
        # self.status_bar.grid()

    def handle_packet(self, bs):
        stuff = iter(bs)
        target = stuff.next()
        if target == REEL_CMD:
            cmd = stuff.next()
            if cmd == ord('i'):
                reel_id = chr(stuff.next())
                reel_bytes = bytearray(stuff)
                try:
                    reel = Reel.from_bytes(reel_bytes)
                except AssertionError as e:
                    print 'nah', e
                    print ' '.join('{:02X}'.format(b) for b in reel_bytes)
                else:
                    print 'got reel info: ', reel_id, reel
                    self.handle_reel_update(reel_id, reel)
            else:
                raise NotImplementedError(
                    'reel command (0x{0:02X} {0:d} {0:c}) not working'.format(
                        cmd))
        elif target == FRAME_CMD:
            cmd = stuff.next()
            if cmd == ord('i'):
                reel_id = chr(stuff.next())
                frame = Reel.frame_from_bytes(bytearray(stuff))
                self.handle_reel_frame_update(reel_id, frame)
            else:
                raise NotImplementedError(
                    'frame command (0x{0:02X} {0:d} {0:c}) not working'.format(
                        cmd))
        else:
            print 'woo got packet:'
            print '\n'.join('  0x{0:02X}  {0:3d}  {0:c}'.format(b) for b in bs)

    def handle_advance_frames(self, reel_id, n):
        print 'advancing', reel_id, n, 'frames'
        self.device.send(k103.advance(reel_id, n))

    def handle_reel_update(self, reel_id, reel):
        assert reel_id in ('C', 'P')
        if reel_id == 'C':
            self.replace_camera_reel(reel, False)
        else:
            self.replace_projector_reel(reel, False)

    def handle_reel_frame_update(self, reel_id, frame):
        assert reel_id in ('C', 'P')
        if reel_id == 'C':
            self.camera_current_frame.set(frame)
        else:
            self.projector_current_frame.set(frame)

    def blah(self, x, y, z):
        print 'blah', x, y, z

    def replace_camera_reel(self, reel, persist=True):
        if self.camera_reel is None:
            self.init_camera_reel(reel)
        else:
            self.camera_reel = reel
            self.camera_reel_widget.update(reel)
        if persist:
            self.device.send(k103.update_reel('C', reel))
        self.camera_current_frame.set(reel.current_frame)
        self.program.update_camera_reel(reel)

    def replace_projector_reel(self, reel, persist=True):
        if self.projector_reel is None:
            self.init_projector_reel(reel)
        else:
            self.projector_reel = reel
            self.projector_reel_widget.update(reel)
        if persist:
            self.device.send(k103.update_reel('P', reel))
        self.projector_current_frame.set(reel.current_frame)
        self.program.update_projector_reel(reel)

    def run_program(self, program, proj_rev=False):
        print 'running program...', program
        for n_cam, n_proj in program:
            print 'camera:'
            k103.capture(self.serial, k103.CAM_SELECT, n_cam)
            print 'projector ({}):'.format('r' if proj_rev else 'f')
            p_cmd = k103.K103_SELECT_R if proj_rev else k103.K103_SELECT
            k103.capture(self.serial, p_cmd, n_proj)

    def update_camera_frame(self, *_):
        self.camera_reel.current_frame = self.camera_current_frame.get()
        self.camera_reel_widget.update_reel(self.camera_reel)

    def update_projector_frame(self, *_):
        self.projector_reel.current_frame = self.projector_current_frame.get()
        self.projector_reel_widget.update_reel(self.projector_reel)
