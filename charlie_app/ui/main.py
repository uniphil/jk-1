import time
import Tkinter as tk
import tkFont

from .reel_widgets import ReelInfo
from .program_widgets import Program
from .status_bar import StatusBar
from .. import k103
from ..reel import FRAME_CMD, REEL_CMD, Reel

PACKET_USER_LOG = 0b11 << 6


class App(tk.Frame):
    def __init__(self, device):
        t_init = time.time()
        tk.Frame.__init__(self, None)
        self.device = device
        setattr(device, 'handle_packet', self.handle_packet)
        self.original_alt_packet_handler = device.handle_alt_mode_packet
        setattr(device, 'handle_alt_mode_packet', self.handle_alt_packet)
        self.original_connection_lost = device.connection_lost
        setattr(device, 'connection_lost', self.handle_connection_lost)
        self.manual_program_active = False
        self.main_program_next = None

        self.exiting = False
        self.bind('<Destroy>', self.handle_destroy)

        self.master.title('Charlie control')
        self.latest_update = tk.StringVar()
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
            self.override_camera_frame, self.handle_advance_frames)
        self.camera_reel_widget.grid(row=1, column=0)

    def init_projector_reel(self, reel):
        self.projector_reel = reel
        self.projector_reel_widget = ReelInfo(
            self.projector_frame, 'projector', self.projector_reel,
            self.projector_current_frame, self.replace_projector_reel,
            self.override_projector_frame, self.handle_advance_frames)
        self.projector_reel_widget.grid(row=1, column=0)

    def handle_destroy(self, e):
        self.exiting = True

    def create_widgets(self):
        self.camera_frame = tk.Frame(self)
        self.projector_frame = tk.Frame(self)
        manual_frame = tk.Frame(self)
        program_frame = tk.Frame(self)
        self.status_bar = StatusBar(
            self, self.latest_update, self.handle_cancel)

        camera_label = tk.Label(
            self.camera_frame,
            text='Camera',
            font=tkFont.Font(size=20),
            pady=10)
        self.camera_reel_widget = None

        projector_label = tk.Label(
            self.projector_frame,
            text='Projector',
            font=tkFont.Font(size=20),
            pady=10)
        self.projector_reel_widget = None

        program_label = tk.Label(
            program_frame, text='Program', font=tkFont.Font(size=20), pady=10)
        self.program = Program(
            program_frame, self.camera_reel, self.camera_current_frame,
            self.projector_reel, self.projector_current_frame,
            self.run_program)

        self.camera_frame.grid(row=0, column=0)
        self.projector_frame.grid(row=0, column=1)
        manual_frame.grid(row=1, column=0, columnspan=2)
        program_frame.grid(row=2, column=0, columnspan=2)

        camera_label.grid(row=0, column=0)
        projector_label.grid(row=0, column=0)

        program_label.grid(row=0, column=0)
        self.program.grid(row=1, column=0)

        # tk.Button(
        #     self, text='Dump',
        #     command=lambda: self.device.send(k103.dump('T'))).grid()

        self.status_bar.grid(columnspan=2, sticky=tk.E+tk.W)

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
                print 'frame update', reel_id, frame
                self.handle_reel_frame_update(reel_id, frame)
            elif cmd == ord('.'):
                reel_id = chr(stuff.next())
                frames = Reel.frame_from_bytes(bytearray(stuff))
                print 'frame advance done', reel_id, frames
                self.handle_advance_done(reel_id, frames)
            elif cmd == ord('x'):
                reel_id = chr(stuff.next())
                self.handle_cancelled(reel_id)
            else:
                raise NotImplementedError(
                    'frame command (0x{0:02X} {0:d} {0:c}) not working'.format(
                        cmd))
        elif target == ord('B'):
            device = stuff.next()
            self.handle_busy(chr(device))
        else:
            print 'woo got unrecognized packet:'
            print '\n'.join('  0x{0:02X}  {0:3d}  {0:c}'.format(b) for b in bs)

    def handle_alt_packet(self, data, mode):
        if mode == PACKET_USER_LOG:
            self.latest_update.set(data)
        else:
            self.original_alt_packet_handler(data, mode)

    def _advance_frames_progress(self, n):
        self.status_bar.update_program_step(n)

    def _advance_frames_done(self):
        self.status_bar.end_program()
        self.manual_program_active = False

    def handle_advance_frames(self, reel_id, n):
        assert self.main_program_next is None
        print 'advancing', reel_id, n, 'frames'
        self.status_bar.define_program(abs(n))
        self.manual_program_active = True
        self.device.send(k103.advance(reel_id, n))

    def handle_advance_done(self, reel_id, n):
        main_active = self.main_program_next is not None
        manual_active = self.manual_program_active
        assert main_active or manual_active
        assert not (main_active and manual_active),\
            'main program or manual program can be active, not both!'
        if main_active:
            self.main_program_next()
        else:
            self._advance_frames_done()
        name = 'projector' if reel_id == 'P' else 'camera'
        self.latest_update.set(
            'advanced {} {} frames in last program step'.format(n, name))

    def handle_busy(self, device):
        print 'busy!', device
        popup = tk.Toplevel()
        popup.title('device busy')
        name = 'projector' if device == 'P' else 'camera'
        text = '{} seems to be busy, try again in a moment?'.format(name)
        frame = tk.Frame(popup)
        frame.pack(expand=True, ipadx=12, ipady=4)
        tk.Label(frame, text=text).pack(ipady=12)
        tk.Button(frame, text='Ok', command=lambda: popup.destroy()).pack()

    def handle_cancel(self):
        if self.main_program_next is not None:
            self.main_program_next = None
            self.program.enable()
        if self.manual_program_active:
            self.manual_program_active = False
        self.device.send(k103.cancel_advances())

    def handle_cancelled(self, device):
        name = 'projector' if device == 'P' else 'camera'
        self.latest_update.set(
            'cancelled advances ({} was last active).'.format(name))
        self.status_bar.end_program()

    def handle_connection_lost(self, exc):
        if self.exiting:
            return
        print 'connection lost!'
        popup = tk.Toplevel()
        popup.title('Connection lost')
        text = 'connection lost :('
        frame = tk.Frame(popup)
        frame.pack(expand=True, ipadx=12, ipady=4)
        tk.Label(frame, text=text).pack(ipady=12)
        tk.Button(frame, text='Ok', command=lambda: popup.destroy()).pack()
        self.original_connection_lost(exc)

    def handle_reel_update(self, reel_id, reel):
        assert reel_id in ('C', 'P')
        if reel_id == 'C':
            self.replace_camera_reel(reel, False)
        else:
            self.replace_projector_reel(reel, False)

    def handle_reel_frame_update(self, reel_id, frame):
        assert reel_id in ('C', 'P')
        if reel_id == 'C':
            diff = frame - self.camera_current_frame.get()
            self.camera_current_frame.set(frame)
        else:
            diff = frame - self.projector_current_frame.get()
            self.projector_current_frame.set(frame)
        if self.manual_program_active:
            self._advance_frames_progress(abs(diff))

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

    def override_camera_frame(self, new_frame):
        self.camera_reel.current_frame = new_frame
        self.replace_camera_reel(self.camera_reel)

    def override_projector_frame(self, new_frame):
        self.projector_reel.current_frame = new_frame
        self.replace_projector_reel(self.projector_reel)

    def _run_camera_program(self, n_cam, n_proj, remaining_program):
        def next_program_step():
            print '{} left'.format(len(remaining_program))
            self._run_program(remaining_program)

        def run_projector_program():
            print 'projector: {}'.format(n_proj)
            self.device.send(k103.advance('P', n_proj))
            self.main_program_next = next_program_step
            # TODO: schedule a checkup
            # self.after(1500 + 1300 * abs(n_proj), next_program_step)

        print 'camera: {}'.format(n_cam)
        self.main_program_next = run_projector_program
        self.device.send(k103.advance('C', n_cam))
        # TODO: schedule a checkup
        # self.after(100 + 900 * abs(n_cam), run_projector_program)

    def _run_program(self, remaining_program):
        self.status_bar.update_program(len(remaining_program))
        try:
            n_cam, n_proj = remaining_program.pop(0)
        except IndexError:
            print 'program done!'
            self.main_program_next = None
            self.status_bar.end_program()
            self.program.enable()
            return
        self._run_camera_program(n_cam, n_proj, remaining_program)

    def run_program(self, program):
        assert self.manual_program_active is False
        print 'run program', program
        self.status_bar.define_program(len(program))
        self.program.disable()
        return self._run_program(program)

    def update_camera_frame(self, *_):
        self.camera_reel.current_frame = self.camera_current_frame.get()
        self.camera_reel_widget.update(self.camera_reel)

    def update_projector_frame(self, *_):
        self.projector_reel.current_frame = self.projector_current_frame.get()
        self.projector_reel_widget.update(self.projector_reel)
