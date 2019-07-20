import time
import Tkinter as tk
import ttk
import tkFont

from reel import Reel


class LIFT(object):
    exposure_options = (
        ('Default', 0),
        ('1/5', 0.25),
        ('1/4', 0.75),
        ('0.3', 0.125),
        ('0.4', 0.225),
        ('0.5', 0.325),
        ('0.6', 0.425),
        ('0.8', 0.625),
        ('1', 0.825),
        ('1.3', 1.125),
        ('1.6', 1.425),
        ('2', 1.825),
        ('2.5', 2.325),
        ('3.2', 3.025),
        ('4', 3.825),
        ('5', 4.825),
        ('6', 5.825),
        ('8', 7.825),
        ('10', 9.825),
        ('13', 12.825),
        ('15', 14.825),
        ('20', 19.825),
        ('25', 24.825),
        ('30', 29.825),
        ('35', 34.825),
        ('40', 39.825),
        ('45', 44.825),
        ('50', 49.825),
        ('55', 55.825),
        ('60', 59.825),
    )


class Charlie(object):
    exposure_options = (('1/4', 0.25),)


class App(tk.Frame):
    total_cam_frames = 0
    total_pro_frames = 0
    grid_pos = 0
    contents_pos = -1

    # Lists for modular interface
    mod_on = []             # Module On/Off toggle
    contents_cam_f = []     # Input field camera frames
    contents_exposure = []  # Extposure time
    mb = []                 # Exposure time drop down menu
    cam_back = []           # Camera direction toggle
    contents_pro_f = []     # Input field projector frames
    pro_back = []           # Projector direction toggle
    cycles = []             # Module cycle count
    exp = 0

    hardware = Charlie()

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.grid()
        self.layout()
        self.head_widgets()
        self.input_widgets()
        self.foot_widgets()

    def layout(self):
        self.seperator_head_1 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperator_head_1.grid(
            column=0, row=0, ipadx=10, padx=5, pady=5, sticky=tk.W)

        self.seperator_head_2 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperator_head_2.grid(
            column=1, row=0, ipadx=10, padx=5, pady=5, sticky=tk.E)

        self.seperator_body_1 = tk.Frame(bd=3, relief=tk.RIDGE)
        self.seperator_body_1.grid(column=0, row=1, padx=5, columnspan=2)

        self.seperator_foot_1 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperator_foot_1.grid(
            column=0, row=2, padx=5, pady=5, sticky=tk.W)

        self.seperator_foot_2 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperator_foot_2.grid(
            column=1, row=2, padx=5, pady=5, sticky=tk.E)

        self.seperator_foot_3 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperator_foot_3.grid(
            column=0, row=3, padx=5, pady=5, sticky=tk.W)

        self.seperator_foot_4 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperator_foot_4.grid(
            column=1, row=3, padx=5, pady=5, sticky=tk.E)

    def head_widgets(self):
        self.head_font = tkFont.Font(size=20)

        self.cam_title = tk.Label(
            self.seperator_head_1, text='Current Camera Frame', width=30)
        self.cam_title.grid(column=0, row=0, columnspan=2)
        self.pro_title = tk.Label(
            self.seperator_head_2, text='Current Projector Frame', width=30)
        self.pro_title.grid(column=2, row=0, columnspan=2)

        self.cam_reset = tk.Button(
            self.seperator_head_1, text='reset', state=tk.NORMAL,
            command=self.cam_countReset)
        self.cam_reset.grid(column=0, row=1)

        self.cam_frames = tk.StringVar()
        self.cam_frames.set(self.total_cam_frames)

        self.cam_count = tk.Label(self.seperator_head_1, font=self.head_font)
        self.cam_count.grid(column=1, row=1, padx=5, sticky=tk.E)
        self.cam_count["textvariable"] = self.cam_frames

        self.pro_reset = tk.Button(
            self.seperator_head_2, text='reset', state=tk.NORMAL,
            command=self.pro_countReset)
        self.pro_reset.grid(column=2, row=1)

        self.pro_frames = tk.StringVar()
        self.pro_frames.set(self.total_pro_frames)

        self.pro_count = tk.Label(self.seperator_head_2, font=self.head_font)
        self.pro_count.grid(column=3, row=1, padx=5, sticky=tk.E)
        self.pro_count["textvariable"] = self.pro_frames

        self.cam_f_label = tk.Label(
            self.seperator_body_1, text='Camera Frames:')
        self.cam_f_label.grid(column=1, row=0, sticky=tk.W)

        self.ex_label = tk.Label(self.seperator_body_1, text='Exposure Time:')
        self.ex_label.grid(column=3, row=0, sticky=tk.W)

        self.pro_f_label = tk.Label(
            self.seperator_body_1, text='Projector Frames:')
        self.pro_f_label.grid(column=5, row=0, sticky=tk.W)

        self.cycles_label = tk.Label(self.seperator_body_1, text='Cycles:')
        self.cycles_label.grid(column=7, row=0, sticky=tk.W)

    def input_widgets(self):
        self.grid_pos += 1
        self.contents_pos += 1

        self.mod_on.append(tk.IntVar())
        self.mod_check = tk.Checkbutton(
            self.seperator_body_1, text="ON/OFF",
            variable=self.mod_on[self.contents_pos], onvalue=1, offvalue=0)
        self.mod_check.grid(column=0, row=self.grid_pos, sticky=tk.W)

        self.contents_cam_f.append(tk.IntVar())
        self.cam_frames = tk.Entry(
            self.seperator_body_1, justify=tk.RIGHT,
            textvariable=self.contents_cam_f[self.contents_pos])
        self.cam_frames.grid(column=1, row=self.grid_pos)

        self.contents_exposure.append(tk.DoubleVar())
        self.mb.append(tk.Menubutton(
            self.seperator_body_1, text='Default',
            relief=tk.RAISED))
        self.mb[self.contents_pos].grid(
            column=3, row=self.grid_pos, padx=5, pady=3, sticky=tk.W)
        self.mb[self.contents_pos].menu = tk.Menu(
            self.mb[self.contents_pos], tearoff=0)
        self.mb[self.contents_pos]['menu'] = self.mb[self.contents_pos].menu

        for label, value in self.hardware.exposure_options:
            self.mb[self.contents_pos].menu.add_radiobutton(
                label=label, value=value, command=self.update,
                variable=self.contents_exposure[self.contents_pos])

        self.cam_back.append(tk.IntVar())
        self.cam_check = tk.Checkbutton(
            self.seperator_body_1, text="Reverse",
            variable=self.cam_back[self.contents_pos], onvalue=1,
            offvalue=0)
        self.cam_check.grid(column=4, row=self.grid_pos, sticky=tk.W)

        self.contents_pro_f.append(tk.IntVar())
        self.pro_frames = tk.Entry(
            self.seperator_body_1, justify=tk.RIGHT,
            textvariable=self.contents_pro_f[self.contents_pos])
        self.pro_frames.grid(column=5, row=self.grid_pos)

        self.pro_back.append(tk.IntVar())
        self.pro_check = tk.Checkbutton(
            self.seperator_body_1, text="Reverse",
            variable=self.pro_back[self.contents_pos], onvalue=1,
            offvalue=0)
        self.pro_check.grid(column=6, row=self.grid_pos, sticky=tk.W)

        self.cycles.append(tk.IntVar())
        self.cycle_block = tk.Entry(
            self.seperator_body_1, justify=tk.RIGHT,
            textvariable=self.cycles[self.contents_pos])
        self.cycle_block.grid(column=7, row=self.grid_pos)

    def foot_widgets(self):
        self.add_button = tk.Button(
            self.seperator_foot_1, text='+', padx=1, pady=1, height=1, width=2,
            command=self.input_widgets)
        self.add_button.grid(column=0, row=0, sticky=tk.W)

        self.run_button = tk.Button(
            self.seperator_foot_3, text='RUN', fg='red',
            command=self.run_program)
        self.run_button.grid(column=0, row=0, sticky=tk.W)

        self.test_button = tk.Button(
            self.seperator_foot_3, text='test', fg='green',
            command=self.testProgram)
        self.test_button.grid(column=1, row=0, sticky=tk.W)

        self.total_cycles_label = tk.Label(
            self.seperator_foot_2, text='Total Cycles:')
        self.total_cycles_label.grid(column=0, row=0)
        self.total_cycles = tk.IntVar()
        self.total_cycle_block = tk.Entry(
            self.seperator_foot_2, justify=tk.RIGHT,
            textvariable=self.total_cycles)
        self.total_cycle_block.grid(column=1, row=0)

        self.man = tk.Button(
            self.seperator_foot_4, text='Manual Mode', command=self.manual)
        self.man.grid(column=0, row=0)
        self.cam_fw = tk.Button(
            self.seperator_foot_4, text='Camera FW', state=tk.NORMAL,
            command=self.cam_forward)
        self.cam_fw.grid(column=1, row=0)
        self.cam_bw = tk.Button(
            self.seperator_foot_4, text='Camera BW', state=tk.NORMAL,
            command=self.cam_backward)
        self.cam_bw.grid(column=2, row=0)
        self.pro_fw = tk.Button(
            self.seperator_foot_4, text='Projector FW', state=tk.NORMAL,
            command=self.pro_forward)
        self.pro_fw.grid(column=3, row=0)
        self.pro_bw = tk.Button(
            self.seperator_foot_4, text='Projector BW', state=tk.NORMAL,
            command=self.pro_backward)
        self.pro_bw.grid(column=4, row=0, sticky=tk.W)

    def update(self):
        # Determine number of modules in interface
        lst_length = len(self.mod_on)
        for a in range(0, lst_length):
            self.mb[a]["text"] = self.contents_exposure[a].get() + .175

    def manual(self):
        self.cam_reset['state'] = tk.DISABLED
        self.pro_reset['state'] = tk.DISABLED
        self.cam_fw['state'] = tk.DISABLED
        self.cam_bw['state'] = tk.DISABLED
        self.pro_fw['state'] = tk.DISABLED
        self.pro_bw['state'] = tk.DISABLED
        input_cam_button = GPIO.input(15)
        input_pro_button = GPIO.input(19)
        input_cam_fb = GPIO.input(23)
        input_pro_fb = GPIO.input(26)
        time.sleep(.5)
        while input_cam_button or input_pro_button is True:
            time.sleep(.5)
            input_cam_button = GPIO.input(15)
            input_pro_button = GPIO.input(19)
            input_cam_fb = GPIO.input(23)
            input_pro_fb = GPIO.input(26)
            if input_cam_button is False:
                if input_cam_fb is False:
                    self.cam_backward()
                else:
                    self.cam_forward()
            if input_pro_button is False:
                if input_pro_fb is False:
                    self.pro_backward()
                else:
                    self.pro_forward()
            if GPIO.input(21) is False:
                self.foot_widgets()
                self.head_widgets()
                break

    def run_program(self):
        # Determine number of modules in interface
        lst_length = len(self.mod_on)
        for a in range(0, self.total_cycles.get()):
            if GPIO.input(21) is False:
                break
            index = 0
            for b in range(0, lst_length):
                for c in range(0, self.cycles[index].get()):
                    if GPIO.input(21) is False:
                        break
                    if self.mod_on[index].get() == 1:
                        for d in range(0, self.contents_cam_f[index].get()):
                            self.exp = self.contents_exposure[index].get()
                            if self.cam_back[index].get() == 0:
                                self.cam_forward()
                            else:
                                self.cam_backward()
                            time.sleep(.5)
                        for e in range(0, self.contents_pro_f[index].get()):
                            if self.pro_back[index].get() == 0:
                                self.pro_forward()
                            else:
                                self.pro_backward()
                            time.sleep(.5)
                index += 1

    def testProgram(self):

        grid1 = 10
        self.window_1 = tk.Toplevel()

        self.canv = tk.Canvas(
            self.window_1, width=500, height=800, scrollregion=(0, 0, 0, 0))
        self.canv.grid()
        self.scroll_y = tk.Scrollbar(
            self.window_1, orient=tk.VERTICAL, command=self.canv.yview)
        self.scroll_y.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canv['yscrollcommand'] = self.scroll_y.set

        # Determine number of modules in interface
        lst_length = len(self.mod_on)

        self.lab1 = tk.Label(self.window_1, text='# of Modules: ')
        self.scroll_win = self.canv.create_window(110, grid1, window=self.lab1)
        self.lab2 = tk.Label(self.window_1, text=lst_length)
        self.scroll_win = self.canv.create_window(400, grid1, window=self.lab2)

        for a in range(0, self.total_cycles.get()):
            index = 0
            grid1 += 30

            self.lab3 = tk.Label(self.window_1, text='Main Loop: ')
            self.scroll_win = self.canv.create_window(
                110, grid1, window=self.lab3)
            self.lab4 = tk.Label(self.window_1, text=a+1)
            self.scroll_win = self.canv.create_window(
                400, grid1, window=self.lab4)

            for b in range(0, lst_length):
                grid1 += 20

                self.lab5 = tk.Label(self.window_1, text='Module: ')
                self.scroll_win = self.canv.create_window(
                    110, grid1, window=self.lab5)
                self.lab6 = tk.Label(self.window_1, text=index+1)
                self.scroll_win = self.canv.create_window(
                    400, grid1, window=self.lab6)

                for c in range(0, self.cycles[index].get()):
                    if self.mod_on[index].get() == 1:
                        for d in range(0, self.contents_cam_f[index].get()):
                            grid1 += 20

                            if self.cam_back[index].get() == 0:
                                self.lab7 = tk.Label(
                                    self.window_1,
                                    text='Camera Forward, Exposure Time: ')
                                self.scroll_win = self.canv.create_window(
                                    110, grid1, window=self.lab7)
                                self.lab8 = tk.Label(
                                    self.window_1,
                                    text=self.contents_exposure[index].get() +
                                    .175)
                                self.scroll_win = self.canv.create_window(
                                    400, grid1, window=self.lab8)

                            else:
                                self.lab7 = tk.Label(
                                    self.window_1,
                                    text='Camera Backward, Exposure Time: ')
                                self.scroll_win = self.canv.create_window(
                                    110, grid1, window=self.lab7)
                                self.lab8 = tk.Label(
                                    self.window_1,
                                    text=self.contents_exposure[index].get() +
                                    .175)
                                self.scroll_win = self.canv.create_window(
                                    400, grid1, window=self.lab8)

                        for e in range(0, self.contents_pro_f[index].get()):
                            grid1 += 20

                            if self.pro_back[index].get() == 0:

                                self.lab9 = tk.Label(
                                    self.window_1, text='Projector Forward')
                                self.scroll_win = self.canv.create_window(
                                    110, grid1, window=self.lab9)

                            else:
                                self.lab10 = tk.Label(
                                    self.window_1, text='Projector Backward')
                                self.scroll_win = self.canv.create_window(
                                    110, grid1, window=self.lab10)
                    else:
                        grid1 += 20

                        self.lab7 = tk.Label(
                            self.window_1, text='Module Skipped')
                        self.scroll_win = self.canv.create_window(
                            110, grid1, window=self.lab7)

                index += 1
                self.canv['scrollregion'] = (0, 0, 0, grid1)

    def cam_forward(self):
        self.total_cam_frames += 1
        self.cam_frames = tk.StringVar()
        self.cam_frames.set(self.total_cam_frames)
        self.cam_count["textvariable"] = self.cam_frames
        GPIO.output(16, True)
        time.sleep(.025)
        input_camPos = GPIO.input(11)
        while input_camPos is True:
            input_camPos = GPIO.input(11)
            input_camET = GPIO.input(13)
            if input_camET is False:
                GPIO.output(16, False)
                time.sleep(self.exp)
                GPIO.output(16, True)
                time.sleep(.025)
            else:
                GPIO.output(16, True)
        GPIO.output(16, False)

    def cam_backward(self):
        self.total_cam_frames -= 1
        self.cam_frames = tk.StringVar()
        self.cam_frames.set(self.total_cam_frames)
        self.cam_count["textvariable"] = self.cam_frames

        GPIO.output(12, True)
        time.sleep(.025)
        input_camPos = GPIO.input(11)
        while input_camPos is True:
            input_camPos = GPIO.input(11)
            input_camET = GPIO.input(13)
            if input_camET is False:
                GPIO.output(12, False)
                time.sleep(self.exp)
                GPIO.output(12, True)
                time.sleep(.025)
            else:
                GPIO.output(12, True)
        GPIO.output(12, False)

    def pro_forward(self):
        self.total_pro_frames += 1
        self.pro_frames = tk.StringVar()
        self.pro_frames.set(self.total_pro_frames)
        self.pro_count["textvariable"] = self.pro_frames

        GPIO.output(22, True)
        time.sleep(.025)
        input_camPos = GPIO.input(7)
        while input_camPos is True:
            input_camPos = GPIO.input(7)
            GPIO.output(22, True)
        GPIO.output(22, False)

    def pro_backward(self):
        self.total_pro_frames -= 1
        self.pro_frames = tk.StringVar()
        self.pro_frames.set(self.total_pro_frames)
        self.pro_count["textvariable"] = self.pro_frames

        GPIO.output(18, True)
        time.sleep(.025)
        input_camPos = GPIO.input(7)
        while input_camPos is True:
            input_camPos = GPIO.input(7)
            GPIO.output(18, True)
        GPIO.output(18, False)

    def cam_countReset(self):
        self.total_cam_frames = 0
        self.cam_frames = tk.StringVar()
        self.cam_frames.set(self.total_cam_frames)
        self.cam_count["textvariable"] = self.cam_frames

    def pro_countReset(self):
        self.total_pro_frames = 0
        self.pro_frames = tk.StringVar()
        self.pro_frames.set(self.total_pro_frames)
        self.pro_count["textvariable"] = self.pro_frames


class LoadReelPopup(tk.Toplevel):
    def __init__(self, device, close):
        tk.Toplevel.__init__(self)
        self.close = close
        self.title('Load {} reel...'.format(device))
        self.bind('<Destroy>', self.handle_destroy)
        self.bind('<Escape>', lambda _: self.cancel())

        frame = ttk.Frame(self)
        frame.pack(fill='both')

        title_label = ttk.Label(frame, text='New {} reel'.format(device))
        title_label.grid(column=1, row=0)

        description_label = ttk.Label(frame, text='Description')
        description_label.grid(column=0, row=1, sticky=tk.E)
        self.description = ttk.Entry(frame)
        self.description.grid(column=1, row=1)
        self.description.focus()

        total_frames_label = ttk.Label(frame, text='Total frames')
        total_frames_label.grid(column=0, row=2, sticky=tk.E)
        self.total_frames = ttk.Entry(frame)
        self.total_frames.grid(column=1, row=2)

        current_frame_label = ttk.Label(frame, text='Initial frame')
        current_frame_label.grid(column=0, row=3, sticky=tk.E)

        self.current_frame = ttk.Entry(frame)
        self.current_frame.grid(column=1, row=3)

        buttons = ttk.Frame(frame)
        buttons.grid(column=0, columnspan=2, row=4)
        cancel = ttk.Button(buttons, text='Cancel', command=self.cancel)
        cancel.pack(side='left')
        save = ttk.Button(buttons, text='Save', command=self.save)
        save.pack(side='right')

    def handle_destroy(self, event):
        if event.widget is self:
            self.cancel()

    def cancel(self):
        self.close(None)

    def save(self):
        now = int(time.time())
        description = self.description.get()
        total_frames = int(self.total_frames.get())
        current_frame = int(self.current_frame.get())
        new_reel = Reel(now, description, total_frames, current_frame)
        self.close(new_reel)


class OverrideFramePopup(tk.Toplevel):
    def __init__(self, device, current_frame, close):
        tk.Toplevel.__init__(self)
        self.current_frame = current_frame
        self.new_current_frame = tk.IntVar()
        self.new_current_frame.set(current_frame.get())
        self.close = close

        self.title('Override current {} frame'.format(device))
        self.bind('<Destroy>', self.handle_destroy)
        self.bind('<Escape>', lambda _: self.cancel())

        frame = ttk.Frame(self)
        frame.pack(fill='both')

        label = ttk.Label(frame, text='Current frame:')
        label.grid(column=0, row=0, sticky=tk.E)
        self.frame = ttk.Entry(frame, textvariable=self.new_current_frame)
        self.frame.grid(column=1, row=0)
        self.frame.focus()

        buttons = ttk.Frame(frame)
        buttons.grid(column=0, columnspan=2, row=1)
        cancel = ttk.Button(buttons, text='Cancel', command=self.cancel)
        cancel.pack(side='left')
        save = ttk.Button(buttons, text='Save', command=self.save)
        save.pack(side='right')

    def handle_destroy(self, event):
        if event.widget is self:
            self.cancel()

    def cancel(self):
        self.close()

    def save(self):
        self.current_frame.set(self.new_current_frame.get())
        self.close()


class ReelInfo(ttk.LabelFrame):
    def __init__(self, master, device, reel, current_frame, update_reel):
        ttk.LabelFrame.__init__(self, master, relief='solid', borderwidth=2)
        self.device = device
        self.current_frame = current_frame
        self.update_reel = update_reel
        self.reel_popup = None
        self.frame_override_popup = None
        self.create_widgets()
        self.update(reel)

    def create_widgets(self):
        top = ttk.Frame()
        top.pack(fill='x')
        self.label = ttk.Label(top)
        self.label.pack(side='left')
        self.load_button = ttk.Button(
            top, text='load new', command=self.load_reel)
        self.load_button.pack(side='right')
        self.config(labelwidget=top)

        count = ttk.Frame(self)
        self.film_frame = ttk.Label(count)
        self.film_frame.pack(side='left')
        self.frame_override_button = ttk.Button(
            count, text='override', command=self.edit_count)
        self.frame_override_button.pack(side='right')
        count.pack(side='top')

        self.loaded = ttk.Label(self)
        self.loaded.pack(side='top')

    def edit_count(self):
        if self.frame_override_popup is not None:
            return
        self.frame_override_popup = OverrideFramePopup(
            self.device, self.current_frame, self.close_override_popup)
        self.frame_override_popup.transient(self)
        self.frame_override_button.config(state=tk.DISABLED)

    def close_override_popup(self):
        self.frame_override_popup.destroy()
        self.frame_override_popup = None
        self.frame_override_button.config(state=tk.NORMAL)

    def load_reel(self):
        if self.reel_popup is not None:
            return
        self.reel_popup = LoadReelPopup(self.device, self.close_load_popup)
        self.reel_popup.transient(self)
        self.load_button.config(state=tk.DISABLED)

    def close_load_popup(self, reel):
        if reel is not None:
            self.update_reel(reel)
        self.reel_popup.destroy()
        self.reel_popup = None
        self.load_button.config(state=tk.NORMAL)

    def update(self, reel):
        self.label.config(text='reel: {}'.format(reel.description))
        self.film_frame.config(text='frame: {} (of {})'.format(
            reel.current_frame, reel.total_frames))
        self.loaded.config(text='loaded: {}'.format(
            time.ctime(reel.loaded_at)))


class A2(ttk.Frame):

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


if __name__ == '__main__':
    # app = App()
    app = A2()
    app.master.title('Charlie Control')
    app.mainloop()
