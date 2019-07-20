import Tkinter as tk
import ttk

from .reel import ReelInfo
from ..reel import Reel

class App(ttk.Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.camera_reel = Reel(1555456657, 'test cam', 1800, 1)
        self.camera_current_frame = tk.IntVar()
        self.camera_current_frame.set(self.camera_reel.current_frame)
        self.camera_current_frame.trace('w', self.update_camera_frame)
        self.camera_enable_manual = tk.BooleanVar()
        self.camera_enable_manual.set(False)
        self.projector_reel = Reel(1555456657, 'test pro', 2400, 870)
        self.projector_current_frame = tk.IntVar()
        self.projector_current_frame.set(self.projector_reel.current_frame)
        self.projector_current_frame.trace('w', self.update_projector_frame)
        self.create_widgets()
        self.pack(fill='both')

    def create_widgets(self):
        self.camera_frame = ttk.Frame(self)
        camera_label = ttk.Label(self.camera_frame, text='Camera')
        camera_label.pack()
        self.camera_reel_widget = ReelInfo(
            self.camera_frame, 'camera', self.camera_reel,
            self.camera_current_frame, self.replace_camera_reel)
        self.camera_reel_widget.pack()

        camera_manual = ttk.Frame(self.camera_frame)
        enable_manual = ttk.Checkbutton(
            camera_manual, variable=self.camera_enable_manual,
            text='Enable manual control')
        enable_manual.pack(side='left')
        self.camera_enable_manual.trace('w', self.blah)
        # enable_manual.bind('<Change>', self.blah)
        camera_manual.pack()

        self.camera_frame.pack(side='left')

        self.projector_frame = ttk.Frame(self)
        projector_label = ttk.Label(self.projector_frame, text='Projector')
        projector_label.pack()
        self.projector_reel_widget = ReelInfo(
            self.projector_frame, 'crojector', self.projector_reel,
            self.projector_current_frame, self.replace_projector_reel)
        self.projector_reel_widget.pack()
        self.projector_frame.pack(side='right')

        self.program_frame = ttk.Frame(self)
        self.program_frame.pack(side='bottom')

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
