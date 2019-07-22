import Tkinter as tk
import ttk

from .reel_widgets import ReelInfo
from .program_widgets import Program
from ..reel import Reel

class App(ttk.Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.master.title('Charlie control')
        self.camera_reel = Reel(1555456657, 'test cam', 1800, 1)
        self.camera_current_frame = tk.IntVar()
        self.camera_current_frame.set(self.camera_reel.current_frame)
        self.camera_current_frame.trace('w', self.update_camera_frame)
        self.camera_enable_manual = tk.BooleanVar()
        self.camera_enable_manual.set(False)
        self.camera_enable_manual.trace('w', self.blah)
        self.projector_reel = Reel(1555456657, 'test pro', 2400, 870)
        self.projector_current_frame = tk.IntVar()
        self.projector_current_frame.set(self.projector_reel.current_frame)
        self.projector_current_frame.trace('w', self.update_projector_frame)
        self.create_widgets()
        self.grid()

    def create_widgets(self):
        camera_frame = ttk.Frame(self)
        projector_frame = ttk.Frame(self)
        manual_frame = ttk.Frame(self)
        program_frame = ttk.Frame(self)

        camera_label = ttk.Label(camera_frame, text='Camera')
        self.camera_reel_widget = ReelInfo(
            camera_frame, 'camera', self.camera_reel,
            self.camera_current_frame, self.replace_camera_reel)

        projector_label = ttk.Label(projector_frame, text='Projector')
        self.projector_reel_widget = ReelInfo(
            projector_frame, 'crojector', self.projector_reel,
            self.projector_current_frame, self.replace_projector_reel)

        enable_manual = ttk.Checkbutton(
            manual_frame, variable=self.camera_enable_manual,
            text='Enable manual control')

        program = Program(program_frame)

        camera_frame.grid(row=0, column=0)
        projector_frame.grid(row=0, column=1)
        manual_frame.grid(row=1, column=0, columnspan=2)
        program_frame.grid(row=2, column=0, columnspan=2)

        camera_label.grid(row=0, column=0)
        self.camera_reel_widget.grid(row=1, column=0)

        projector_label.grid(row=0, column=0)
        self.projector_reel_widget.grid(row=1, column=0)

        enable_manual.grid(row=0, column=0)

        program.grid()

    def blah(self, x, y, z):
        print 'blah', x, y, z

    def replace_camera_reel(self, reel):
        self.camera_reel = reel
        self.camera_reel_widget.update(reel)

    def replace_projector_reel(self, reel):
        self.projector_reel = reel
        self.projector_reel_widget.update(reel)

    def update_camera_frame(self, *_):
        self.camera_reel.current_frame = self.camera_current_frame.get()
        self.camera_reel_widget.update_reel(self.camera_reel)

    def update_projector_frame(self, *_):
        self.projector_reel.current_frame = self.projector_current_frame.get()
        self.projector_reel_widget.update_reel(self.projector_reel)

    def heya(self):
        print 'sup', self
