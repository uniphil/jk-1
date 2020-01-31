# -*- coding: utf-8 -*-
import Tkinter as tk
import tkFont
from scrollable_frame import ScrollableFrame


BG = '#f2f2f2'
ROW_BG = '#e6e6e6'


class Cycle(tk.Frame):
    def __init__(self, master, index=0, **kwargs):
        tk.Frame.__init__(
            self, master, **kwargs)
        self.actions = []
        self.cycles_count = tk.StringVar()
        self.cycles_count.set('1')

        count_bg = '#f0e0f8'
        big = tkFont.Font(size=24)
        small = tkFont.Font(size=11)

        count_frame = tk.Frame(self, background=count_bg)
        count_frame.grid(row=0, column=0, rowspan=2, sticky=tk.N+tk.S+tk.W)
        count_label = tk.Label(count_frame, text='Step', background=count_bg)
        count_label.grid(
            row=0, column=0, columnspan=2, sticky=tk.E+tk.W, pady=(16, 0))
        self.count_index = tk.Label(
            count_frame, text=index+1, background=count_bg, width=7,
            font=big)
        self.count_index.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)

        self.count_value = tk.Entry(
            count_frame, textvariable=self.cycles_count, width=3,
            highlightthickness=0, borderwidth=1, justify='center')
        self.count_value.grid(row=2, column=0, pady=16, stick=tk.S+tk.E)
        self.count_value.bind('<FocusIn>', self.handle_focus_count)
        tk.Label(
            count_frame, text='repeat', background=count_bg,
            font=small
        ).grid(row=2, column=1, pady=16, sticky=tk.S+tk.W)
        count_frame.rowconfigure(2, weight=1)

        self.actions_frame = tk.Frame(self)
        self.no_actions_label = tk.Label(
            self.actions_frame,
            text='Add an action to activate this cycle',
            font=tkFont.Font(slant='italic'),
            foreground='#777',
            background='#e6fae3')
        self.no_actions_label.grid(row=0, column=0, ipady=6, sticky=tk.E+tk.W)
        self.actions_frame.columnconfigure(0, weight=1)

        self.actions_frame.grid(
            row=0, column=1, padx=6, pady=6, sticky=tk.E+tk.W)
        self.columnconfigure(1, weight=1)

        add_actions_frame = tk.Frame(self)
        add_actions_frame.grid(row=1, column=1)

        actions_label = tk.Label(add_actions_frame, text='Actions:')
        actions_label.grid(row=0, column=0)

        camera_cam_button = tk.Button(
            add_actions_frame,
            text='+ Camera',
            command=self.add_camera_action)
        camera_cam_button.grid(row=0, column=1)
        camera_proj_button = tk.Button(
            add_actions_frame,
            text='+ Projector',
            command=self.add_projector_action)
        camera_proj_button.grid(row=0, column=2)

    def handle_focus_count(self, *_):
        self.count_value.focus()
        self.count_value.select_range(0, tk.END)

    def _get_action(self):
        self.no_actions_label.grid_forget()
        action_index = len(self.actions)
        action = tk.Frame(self.actions_frame, background=ROW_BG)
        action.grid(
            row=action_index, column=0, sticky=tk.E+tk.W, pady=2)
        action_number = tk.Label(
            action,
            text=chr(ord('A') + action_index),
            font=tkFont.Font(size=21),
            background='#ffc',
            width=2)
        setattr(action, 'action_number', action_number)
        control_frame = tk.Frame(action)
        control_frame.grid(row=0, column=1)
        remove = tk.Button(
            action, text='✕', highlightbackground=ROW_BG,
            command=lambda: self.remove_action(action))
        remove.grid(row=0, column=2, sticky=tk.E)
        action.columnconfigure(1, weight=1)
        action_number.grid(row=0, column=0, sticky=tk.N+tk.S)
        self.actions.append(action)
        return control_frame

    def add_camera_action(self):
        control_frame = self._get_action()
        action = tk.Label(
            control_frame, text='Camera:', background=ROW_BG,
            font=tkFont.Font(weight='bold'))
        action.grid(row=0, column=0)

    def add_projector_action(self):
        control_frame = self._get_action()
        projector = tk.Label(
            control_frame, text='Projector:', background=ROW_BG,
            font=tkFont.Font(weight='bold'))
        projector.grid(row=0, column=0)

    def remove_action(self, action):
        self.actions = [a for a in self.actions if a is not action]
        action.destroy()
        for i, action in enumerate(self.actions):
            action.action_number.configure(text=chr(ord('A') + i))
            action.grid(row=i, column=0, sticky=tk.E+tk.W)
        if len(self.actions) == 0:
            self.no_actions_label.grid(
                row=0, column=0, ipady=6, sticky=tk.E+tk.W)


class Program(tk.Frame):
    def __init__(self, master, on_run, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.on_run = on_run
        self.cycles = []
        self.create_widgets()

    def create_widgets(self):
        self.cycles_frame = ScrollableFrame(self, background=BG)
        self.cycles_list = tk.Frame(
            self.cycles_frame.scrollable_frame, background=BG)
        self.cycles_list.grid(row=0, column=0, sticky=tk.E+tk.W)
        self.cycles_list.columnconfigure(0, weight=1)
        cycle = Cycle(self.cycles_list, borderwidth=1, relief='raised')
        self.cycles.append(cycle)
        cycle.grid(row=0, column=0, pady=(0, 6), sticky=tk.E+tk.W)

        cycles_buttons = tk.Frame(
            self.cycles_frame.scrollable_frame, background=BG)
        cycles_buttons.grid(row=1, column=0, pady=(16, 24))
        tk.Button(
            cycles_buttons, text='+ Step', highlightbackground=BG,
            command=self.add_step,
        ).grid(row=0, column=0)

        self.cycles_frame.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.cycles_frame.scrollable_frame.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def add_step(self):
        cycle_index = len(self.cycles)
        cycle = Cycle(
            self.cycles_list, cycle_index,borderwidth=1, relief='raised')
        cycle.grid(row=cycle_index, column=0, pady=(0, 6), sticky=tk.E+tk.W)
        self.cycles.append(cycle)

        # camera_total_frames_entry.bind('<KeyRelease>', self.set_camera_frames)
        # camera_total_frames_entry.bind('<FocusOut>', self.set_camera_frames)
        # camera_total_frames_label.grid(row=0, column=0)
        # camera_total_frames_entry.grid(row=0, column=1)
        # self.camera_frames_label.grid(row=1, column=0, columnspan=2)

        # ratio_label = tk.Label(rate_frame, text='Frame ratio:')
        # faster_button = tk.Button(
        #     rate_frame, text='←', command=self.adjust_rate_slower, width=1)
        # self.rate_label = tk.Label(rate_frame)
        # slower_button = tk.Button(
        #     rate_frame, text='→', command=self.adjust_rate_faster, width=1)
        # self.frame_ratio_text = tk.Label(rate_frame, text='asdf')
        # ratio_label.grid(row=0, column=0)
        # faster_button.grid(row=0, column=1)
        # self.rate_label.grid(row=0, column=2)
        # slower_button.grid(row=0, column=3)
        # self.frame_ratio_text.grid(row=1, column=0, columnspan=5)

        # projector_total_frames_label = tk.Label(
        #     projector_frame, text='Projector frames')
        # projector_reverse_option = tk.Checkbutton(
        #     projector_frame, text='Reverse', variable=self.projector_reverse)
        # self.projector_frames_label = tk.Label(projector_frame)

        # projector_total_frames_label.grid(row=0, column=0)
        # projector_reverse_option.grid(row=0, column=2)
        # self.projector_frames_label.grid(row=1, column=0, columnspan=3)

        # self.run_button = tk.Button(
        #     self, text='Run program', command=self.run_program)

        # title.grid(row=0, column=0, columnspan=3)

        # camera_frame.grid(row=1, column=0, padx=6)
        # rate_frame.grid(row=1, column=1, padx=24)
        # projector_frame.grid(row=1, column=2, padx=6)

        # self.run_button.grid(row=2, column=0, columnspan=3)

        # self.update_rate()
        # self.grid()

    # def disable(self):
    #     self.run_button.config(state=tk.DISABLED, text='Program running...')

    # def enable(self):
    #     self.run_button.config(state=tk.NORMAL, text='Run program')

    # def run_program(self):
    #     print 'go time'
    #     cam_frames = self.camera_total_frames.get()
    #     if cam_frames == '':
    #         # TODO: alert
    #         return
    #     cam_frames = int(cam_frames)
    #     # proj_frames = self.projector_total_frames.get()
    #     proj_frames = 1  # FIXME
    #     rate = self.rate_adjust.get()
    #     proj_direction = -1 if self.projector_reverse.get() else 1
    #     if self.rate_inverse.get():
    #         program = [(rate, 1 * proj_direction) for _ in range(proj_frames)]
    #     else:
    #         program = [(1, rate * proj_direction) for _ in range(cam_frames)]
    #     self.on_run(program)

    # def update_camera_reel(self, reel):
    #     self.camera_reel = reel
    #     # self.update_camera_frame_label()

    # def update_projector_reel(self, reel):
    #     self.projector_reel = reel
    #     # self.update_projector_frame_label()
