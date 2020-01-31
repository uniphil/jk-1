# -*- coding: utf-8 -*-
import Tkinter as tk
import tkFont
from scrollable_frame import ScrollableFrame


BG = '#f2f2f2'
STEP_HL = '#f0e0f8'
ACTION_HL = '#e6fae3'


class DeviceAction(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.frames = tk.StringVar()
        self.frames.set('1')

        self.smol = tkFont.Font(size=12)

        self.frames_entry = tk.Entry(
            self, textvariable=self.frames, width=5,
            justify='center')
        self.frames_entry.grid(
            row=0, column=0, sticky=tk.W+tk.N+tk.S, ipadx=0, padx=0)
        self.frames_entry.bind('<FocusIn>', self.select_frames_entry)

        frames_label = tk.Label(
            self, text='frame', font=self.smol)
        frames_label.grid(row=0, column=1, sticky=tk.N+tk.S, padx=(0, 12))

    def select_frames_entry(self, *_):
        self.frames_entry.select_range(0, tk.END)


class CameraAction(DeviceAction):
    name = 'Camera'

    def __init__(self, master, **kwargs):
        DeviceAction.__init__(self, master, **kwargs)


class ProjectorAction(DeviceAction):
    name = 'Projector'

    def __init__(self, master, **kwargs):
        DeviceAction.__init__(self, master, **kwargs)

        self.direction = tk.StringVar()
        self.direction.set('fw')

        fw_radio = tk.Radiobutton(
            self, text='advance', value='fw', variable=self.direction,
            font=self.smol)
        fw_radio.grid(row=0, column=2)

        rw_radio = tk.Radiobutton(
            self, text='reverse', value='rw', variable=self.direction,
            font=self.smol)
        rw_radio.grid(row=0, column=3)


class Cycle(tk.Frame):
    def __init__(self, master, index=0, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.actions = []
        self.cycles_count = tk.StringVar()
        self.cycles_count.set('1')

        self.big = tkFont.Font(size=24)
        self.med = tkFont.Font(size=18)
        self.smol = tkFont.Font(size=10, weight='bold')
        self.smolnb = tkFont.Font(size=10)

        count_frame = tk.Frame(self, background=STEP_HL)
        count_frame.grid(row=0, column=0, rowspan=2, sticky=tk.N+tk.S+tk.W)
        count_label = tk.Label(count_frame, text='Step', background=STEP_HL)
        count_label.grid(
            row=0, column=0, columnspan=2, sticky=tk.E+tk.W, pady=(16, 0))
        self.count_index = tk.Label(
            count_frame, text=index+1, background=STEP_HL, width=7,
            font=self.big)
        self.count_index.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)

        self.count_value = tk.Entry(
            count_frame, textvariable=self.cycles_count, width=4,
            highlightthickness=0, borderwidth=1, justify='center')
        self.count_value.grid(row=2, column=1, pady=16, stick=tk.N+tk.W)
        self.count_value.bind('<FocusIn>', self.handle_focus_count)
        tk.Label(
            count_frame, text='repeat', background=STEP_HL,
            font=self.smolnb
        ).grid(row=2, column=0, pady=16, sticky=tk.N+tk.E)
        count_frame.rowconfigure(2, weight=1)

        self.actions_frame = tk.Frame(self)
        self.no_actions_label = tk.Label(
            self.actions_frame,
            text='Add an action to activate this step',
            font=tkFont.Font(slant='italic'),
            foreground='#777',
            background=ACTION_HL)
        self.no_actions_label.grid(
            row=0, column=0, pady=(8, 0), ipady=6, sticky=tk.E+tk.W)
        self.actions_frame.columnconfigure(0, weight=1)

        self.actions_frame.grid(
            row=0, column=1, padx=6, pady=6, sticky=tk.E+tk.W)
        self.columnconfigure(1, weight=1)

        add_actions_frame = tk.Frame(self)
        add_actions_frame.grid(row=1, column=1)

        camera_cam_button = tk.Button(
            add_actions_frame,
            text='+ Camera action',
            command=lambda: self.add_action(CameraAction))
        camera_cam_button.grid(row=0, column=0)
        camera_proj_button = tk.Button(
            add_actions_frame,
            text='+ Projector action',
            command=lambda: self.add_action(ProjectorAction))
        camera_proj_button.grid(row=0, column=1)

    def handle_focus_count(self, *_):
        self.count_value.focus()
        self.count_value.select_range(0, tk.END)

    def add_action(self, cls):
        self.no_actions_label.grid_forget()
        action_index = len(self.actions)
        action_border = tk.Frame(self.actions_frame, background='#eee')
        action_border.grid(
            row=action_index, column=0, pady=4, sticky=tk.N+tk.S+tk.E+tk.W)
        action_border.columnconfigure(0, weight=1)
        action = tk.Frame(action_border)
        action.grid(
            row=0, column=0, sticky=tk.E+tk.W, pady=(0, 1))
        name = tk.Label(
            action, text=cls.name.upper(), background=ACTION_HL,
            font=self.smol)
        name.grid(row=0, column=0, sticky=tk.N+tk.W, ipadx=4)
        control_frame = tk.Frame(action)
        control_frame.grid(row=1, column=0, columnspan=2, pady=2, sticky=tk.W)
        remove = tk.Label(
            action, text='✕', foreground='#777', width=3, font=self.smol,
            justify=tk.CENTER)
        remove.bind('<Button-1>', lambda _: self.remove_action(action_border))
        remove.grid(row=0, column=1, rowspan=2, sticky=tk.N+tk.W)
        action.columnconfigure(1, weight=1)
        self.actions.append(action_border)
        device_action = cls(control_frame)
        device_action.grid(row=0, column=0, padx=6)
        setattr(action_border, 'action', device_action)

    def remove_action(self, action):
        self.actions = [a for a in self.actions if a is not action]
        action.destroy()
        for i, action in enumerate(self.actions):
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
        cycle.grid(row=0, column=0, pady=(0, 16), sticky=tk.E+tk.W)

        cycles_buttons = tk.Frame(
            self.cycles_frame.scrollable_frame, background=BG)
        cycles_buttons.grid(row=1, column=0, pady=(16, 24))
        tk.Button(
            cycles_buttons, text='+ Step', highlightbackground=BG,
            command=self.add_step,
        ).grid(row=0, column=0)
        self.run_button = tk.Button(
            cycles_buttons, text='Run Program', highlightbackground=BG,
            font=tkFont.Font(weight='bold'),
            command=self.run_program)
        self.run_button.grid(row=0, column=1, ipady=6)

        self.cycles_frame.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.cycles_frame.scrollable_frame.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def add_step(self):
        cycle_index = len(self.cycles)
        cycle = Cycle(
            self.cycles_list, cycle_index, borderwidth=1, relief='raised')
        cycle.grid(row=cycle_index, column=0, pady=(0, 16), sticky=tk.E+tk.W)
        rm = tk.Label(
            cycle, text='✕', foreground='#833', width=2, justify=tk.CENTER)
        rm.place(relx=1, anchor=tk.NE)
        rm.bind('<Button-1>', lambda _: self.remove_step(cycle))
        self.cycles.append(cycle)

    def remove_step(self, cycle):
        self.cycles = [a for a in self.cycles if a is not cycle]
        cycle.destroy()
        for i, cycle in enumerate(self.cycles):
            cycle.grid(row=i, column=0, sticky=tk.E+tk.W)

    def run_program(self):
        program = []
        for cycle in self.cycles:
            for _ in range(int(cycle.cycles_count.get())):
                for a in cycle.actions:
                    n = int(a.action.frames.get())
                    if a.action.name == 'Camera':
                        program.append((n, 0))
                    else:
                        if a.action.direction.get() == 'rw':
                            n *= -1
                        program.append((0, n))
        self.on_run(program)

    def disable(self):
        self.run_button.config(state=tk.DISABLED, text='Program running...')

    def enable(self):
        self.run_button.config(state=tk.NORMAL, text='Run program')
