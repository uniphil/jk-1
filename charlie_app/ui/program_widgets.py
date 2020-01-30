# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk


class Program(ttk.Frame):
    def __init__(
        self, master, camera_reel, camera_current_frame,
        projector_reel, projector_current_frame, on_run,
    ):
        ttk.Frame.__init__(self, master)
        self.camera_reel = camera_reel
        self.camera_current_frame = camera_current_frame
        self.projector_reel = projector_reel
        self.projector_current_frame = projector_current_frame
        self.on_run = on_run

        self.camera_total_frames = tk.StringVar()
        self.camera_total_frames.set(1)
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
            camera_frame, textvariable=self.camera_total_frames, width=4)
        self.camera_frames_label = ttk.Label(camera_frame)

        camera_total_frames_entry.bind('<KeyRelease>', self.set_camera_frames)
        camera_total_frames_entry.bind('<FocusOut>', self.set_camera_frames)
        camera_total_frames_label.grid(row=0, column=0)
        camera_total_frames_entry.grid(row=0, column=1)
        self.camera_frames_label.grid(row=1, column=0, columnspan=2)

        ratio_label = ttk.Label(rate_frame, text='Frame ratio:')
        faster_button = ttk.Button(
            rate_frame, text='←', command=self.adjust_rate_slower, width=1)
        self.rate_label = ttk.Label(rate_frame)
        slower_button = ttk.Button(
            rate_frame, text='→', command=self.adjust_rate_faster, width=1)
        self.frame_ratio_text = ttk.Label(rate_frame, text='asdf')
        ratio_label.grid(row=0, column=0)
        faster_button.grid(row=0, column=1)
        self.rate_label.grid(row=0, column=2)
        slower_button.grid(row=0, column=3)
        self.frame_ratio_text.grid(row=1, column=0, columnspan=5)

        projector_total_frames_label = ttk.Label(
            projector_frame, text='Projector frames')
        projector_reverse_option = ttk.Checkbutton(
            projector_frame, text='Reverse', variable=self.projector_reverse)
        self.projector_frames_label = ttk.Label(projector_frame)

        projector_total_frames_label.grid(row=0, column=0)
        projector_reverse_option.grid(row=0, column=2)
        self.projector_frames_label.grid(row=1, column=0, columnspan=3)

        self.run_button = ttk.Button(
            self, text='Run program', command=self.run_program)

        title.grid(row=0, column=0, columnspan=3)

        camera_frame.grid(row=1, column=0, padx=6)
        rate_frame.grid(row=1, column=1, padx=24)
        projector_frame.grid(row=1, column=2, padx=6)

        self.run_button.grid(row=2, column=0, columnspan=3)

        self.update_rate()

    def set_camera_frames(self, *args):
        rate = self.rate_adjust.get()
        camera_frames = self.camera_total_frames.get()
        if self.rate_inverse.get():
            projector_frames = camera_frames / rate
        else:
            projector_frames = camera_frames * rate
        # self.projector_total_frames.set(projector_frames)
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

    def disable(self):
        self.run_button.config(state=tk.DISABLED, text='Program running...')

    def enable(self):
        self.run_button.config(state=tk.NORMAL, text='Run program')

    def run_program(self):
        print 'go time'
        cam_frames = self.camera_total_frames.get()
        if cam_frames == '':
            # TODO: alert
            return
        cam_frames = int(cam_frames)
        # proj_frames = self.projector_total_frames.get()
        proj_frames = 1  # FIXME
        rate = self.rate_adjust.get()
        proj_direction = -1 if self.projector_reverse.get() else 1
        if self.rate_inverse.get():
            program = [(rate, 1 * proj_direction) for _ in range(proj_frames)]
        else:
            program = [(1, rate * proj_direction) for _ in range(cam_frames)]
        self.on_run(program)

    def update_rate(self, *args):
        rate = self.rate_adjust.get()
        # if rate is None None None None None None
        cam, proj = (rate, 1) if self.rate_inverse.get() else (1, rate)
        ratio = '{}:{}'.format(cam, proj)
        ratio_text = 'Advance {} camera frames for every '\
            '{} projector frames.'.format(cam, proj)
        self.rate_label.config(text=ratio)
        self.frame_ratio_text.config(text=ratio_text)
        self.set_camera_frames()
        self.update_camera_frame_label()
        self.update_projector_frame_label()

    def update_camera_frame_label(self, *args):
        camera_frames = int(self.camera_total_frames.get() or '1')
        start_frame = self.camera_current_frame.get()
        end_frame = start_frame + camera_frames
        use = float(camera_frames) / self.camera_reel.total_frames\
            if self.camera_reel is not None else 0
        self.camera_frames_label.config(
            text='Frame {}–{} ({:.1%} of reel)'.format(
                start_frame, end_frame, use))

    def update_projector_frame_label(self, *args):
        # frames = self.projector_total_frames.get()
        frames = 1  # fixme
        reverse = self.projector_reverse.get()
        start_frame = self.camera_current_frame.get()
        end_frame = start_frame + (-frames if reverse else frames)
        use = float(frames) / self.projector_reel.total_frames\
            if self.projector_reel is not None else 0
        self.projector_frames_label.config(
            text='Frame {}–{} ({:.1%} of reel)'.format(
                start_frame, end_frame, use))

    def update_camera_reel(self, reel):
        self.camera_reel = reel
        self.update_camera_frame_label()

    def update_projector_reel(self, reel):
        self.projector_reel = reel
        self.update_projector_frame_label()
