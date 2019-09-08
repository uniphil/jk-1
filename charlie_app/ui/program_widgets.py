# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk


class Program(ttk.Frame):
    def __init__(self, master, camera_reel, projector_reel, on_run):
        ttk.Frame.__init__(self, master)
        self.camera_reel = camera_reel
        self.projector_reel = projector_reel
        self.on_run = on_run

        self.camera_total_frames = tk.IntVar()
        self.camera_total_frames.set(1)
        self.projector_total_frames = tk.IntVar()
        self.projector_total_frames.set(1)
        self.projector_reverse = tk.BooleanVar()
        self.projector_reverse.set(False)

        self.rate_adjust = tk.IntVar()
        self.rate_adjust.set(1)
        self.rate_inverse = tk.BooleanVar()
        self.rate_inverse.set(False)

        self.rate_adjust.trace('w', self.update_rate)
        self.rate_inverse.trace('w', self.update_rate)
        self.projector_reverse.trace('w', self.update_rate)

        self.create_widgets()

    def create_widgets(self):
        self.config(relief='solid', borderwidth=2)
        title = ttk.Label(self, text='Printing program')

        camera_frame = ttk.Frame(self)
        rate_frame = ttk.Frame(self)
        projector_frame = ttk.Frame(self)

        camera_total_frames_label = ttk.Label(
            camera_frame, text='Camera frames:')
        camera_total_frames_entry = ttk.Entry(
            camera_frame, textvariable=self.camera_total_frames, width=8)
        self.camera_frames_label = ttk.Label(camera_frame)

        camera_total_frames_entry.bind('<KeyRelease>', self.set_camera_frames)
        camera_total_frames_entry.bind('<FocusOut>', self.set_camera_frames)
        camera_total_frames_label.grid(row=0, column=0)
        camera_total_frames_entry.grid(row=0, column=1)
        self.camera_frames_label.grid(row=1, column=0, columnspan=2)

        faster_button = ttk.Button(
            rate_frame, text='Faster', command=self.adjust_rate_faster)
        self.rate_label = ttk.Label(rate_frame)
        slower_button = ttk.Button(
            rate_frame, text='Slower', command=self.adjust_rate_slower)
        faster_button.grid(row=0, column=0)
        self.rate_label.grid(row=1, column=0)
        slower_button.grid(row=2, column=0)

        projector_total_frames_label = ttk.Label(
            projector_frame, text='Projector frames')
        projector_total_frames_entry = ttk.Entry(
            projector_frame, textvariable=self.projector_total_frames, width=8)
        projector_reverse_option = ttk.Checkbutton(
            projector_frame, text='Reverse', variable=self.projector_reverse)
        self.projector_frames_label = ttk.Label(projector_frame)

        projector_total_frames_entry.bind(
            '<KeyRelease>', self.set_projector_frames)
        projector_total_frames_entry.bind(
            '<FocusOut>', self.set_projector_frames)
        projector_total_frames_label.grid(row=0, column=0)
        projector_total_frames_entry.grid(row=0, column=1)
        projector_reverse_option.grid(row=0, column=2)
        self.projector_frames_label.grid(row=1, column=0, columnspan=3)

        run_button = ttk.Button(
            self, text='Run program', command=self.run_program)

        title.grid(row=0, column=0, columnspan=3)

        camera_frame.grid(row=1, column=0)
        rate_frame.grid(row=1, column=1)
        projector_frame.grid(row=1, column=2)

        run_button.grid(row=2, column=0, columnspan=3)

        self.update_rate()

    def set_camera_frames(self, *args):
        rate = self.rate_adjust.get()
        camera_frames = self.camera_total_frames.get()
        if self.rate_inverse.get():
            projector_frames = camera_frames / rate
        else:
            projector_frames = camera_frames * rate
        self.projector_total_frames.set(projector_frames)
        self.update_camera_frame_label()
        self.update_projector_frame_label()

    def set_projector_frames(self, *args):
        rate = self.rate_adjust.get()
        projector_frames = self.projector_total_frames.get()
        if self.rate_inverse.get():
            camera_frames = projector_frames * rate
        else:
            camera_frames = projector_frames / rate
        self.camera_total_frames.set(camera_frames)
        self.update_camera_frame_label()
        self.update_projector_frame_label()

    def adjust_rate_slower(self, *args):
        current_rate = self.rate_adjust.get()
        if current_rate == 1:
            self.rate_inverse.set(True)
        current_rate += 1 if self.rate_inverse.get() else -1
        self.rate_adjust.set(current_rate)
        self.update_camera_frame_label()
        self.update_projector_frame_label()

    def adjust_rate_faster(self, *args):
        current_rate = self.rate_adjust.get()
        if current_rate == 1:
            self.rate_inverse.set(False)
        current_rate += -1 if self.rate_inverse.get() else 1
        self.rate_adjust.set(current_rate)
        self.update_camera_frame_label()
        self.update_projector_frame_label()

    def run_program(self):
        print 'go time'
        cam_frames = self.camera_total_frames.get()
        proj_frames = self.projector_total_frames.get()
        rate = self.rate_adjust.get()
        if self.rate_inverse.get():
            program = [(rate, 1) for _ in range(proj_frames)]
        else:
            program = [(1, rate) for _ in range(cam_frames)]
        projector_reverse = self.projector_reverse.get()
        self.on_run(program, projector_reverse)

    def update_rate(self, *args):
        rate = self.rate_adjust.get()
        if self.rate_inverse.get():
            ratio = '{}:1'.format(rate)
        else:
            ratio = '1:{}'.format(rate)
        self.rate_label.config(text=ratio)
        self.set_camera_frames()
        self.update_camera_frame_label()
        self.update_projector_frame_label()

    def update_camera_frame_label(self, *args):
        camera_frames = self.camera_total_frames.get()
        start_frame = 0  # self.camera_reel.current_frame
        end_frame = start_frame + camera_frames
        use = 0  # float(camera_frames) / self.camera_reel.total_frames
        self.camera_frames_label.config(
            text='Frame {}–{} ({:.1%} of reel)'.format(
                start_frame, end_frame, use))

    def update_projector_frame_label(self, *args):
        frames = self.projector_total_frames.get()
        reverse = self.projector_reverse.get()
        start_frame = 0  #self.projector_reel.current_frame
        end_frame = start_frame + (-frames if reverse else frames) 
        use = 0  # float(frames) / self.projector_reel.total_frames
        self.projector_frames_label.config(
            text='Frame {}–{} ({:.1%} of reel)'.format(
                start_frame, end_frame, use))

    def update_camera_reel(self, reel):
        self.camera_reel = reel
        self.update_camera_frame_label()

    def update_projector_reel(self, reel):
        self.projector_reel = reel
        self.update_projector_frame_label()
