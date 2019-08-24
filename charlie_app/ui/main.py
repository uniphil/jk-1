import time
import Tkinter as tk
import ttk
from serial import Serial

from .reel_widgets import ReelInfo
from .program_widgets import Program
from .status_bar import StatusBar
from ..reel import Reel
from .. import k103


class App(ttk.Frame):
    def __init__(self, serial_port=None):
        ttk.Frame.__init__(self, None)
        self.serial = None
        self.master.title('Charlie control')
        self.camera_reel = Reel(1555456657, 'demo camera reel', 1800, 1)
        self.camera_current_frame = tk.IntVar()
        self.camera_current_frame.set(self.camera_reel.current_frame)
        self.camera_current_frame.trace('w', self.update_camera_frame)
        self.projector_reel = Reel(1555456657, 'demo projector reel', 2400, 1)
        self.projector_current_frame = tk.IntVar()
        self.projector_current_frame.set(self.projector_reel.current_frame)
        self.projector_current_frame.trace('w', self.update_projector_frame)
        self.create_widgets()
        self.grid()
        if serial_port is not None:
            self.connect_serial(serial_port)

    def create_widgets(self):
        camera_frame = ttk.Frame(self)
        projector_frame = ttk.Frame(self)
        manual_frame = ttk.Frame(self)
        program_frame = ttk.Frame(self)
        status_bar_frame = ttk.Frame(self)

        camera_label = ttk.Label(camera_frame, text='Camera')
        self.camera_reel_widget = ReelInfo(
            camera_frame, 'camera', self.camera_reel,
            self.camera_current_frame, self.replace_camera_reel)

        projector_label = ttk.Label(projector_frame, text='Projector')
        self.projector_reel_widget = ReelInfo(
            projector_frame, 'crojector', self.projector_reel,
            self.projector_current_frame, self.replace_projector_reel)

        self.program = Program(
            program_frame, self.camera_reel, self.projector_reel,
            self.run_program)

        self.status_bar = StatusBar(
            status_bar_frame, self.connect_serial)

        camera_frame.grid(row=0, column=0)
        projector_frame.grid(row=0, column=1)
        manual_frame.grid(row=1, column=0, columnspan=2)
        program_frame.grid(row=2, column=0, columnspan=2)
        status_bar_frame.grid(row=3, column=0, columnspan=2)

        camera_label.grid(row=0, column=0)
        self.camera_reel_widget.grid(row=1, column=0)

        projector_label.grid(row=0, column=0)
        self.projector_reel_widget.grid(row=1, column=0)

        self.program.grid()
        self.status_bar.grid()

    def connect_serial(self, serial_port):
        self.serial = Serial(serial_port, 9600)
        time.sleep(1)
        t = self.serial.read(self.serial.in_waiting)
        print 'dump serial buff:', t

    def blah(self, x, y, z):
        print 'blah', x, y, z

    def replace_camera_reel(self, reel):
        self.camera_reel = reel
        self.camera_reel_widget.update(reel)
        self.program.update_camera_reel(reel)

    def replace_projector_reel(self, reel):
        self.projector_reel = reel
        self.projector_reel_widget.update(reel)
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
