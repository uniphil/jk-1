import Tkinter as tk
from datetime import date
import time
import tkFont

from ..reel import Reel


class ReplaceReelPopup(tk.Toplevel):
    def __init__(self, device, close):
        tk.Toplevel.__init__(self)
        self.close = close
        self.title('Replace {} reel...'.format(device))
        self.bind('<Destroy>', self.handle_destroy)
        self.bind('<Escape>', lambda _: self.cancel())

        frame = tk.Frame(self, padx=8, pady=4)
        frame.pack(fill='both')

        title_label = tk.Label(
            frame, text='New {} reel'.format(device),
            font=tkFont.Font(size=20),
            pady=10)
        title_label.grid(column=0, row=0, columnspan=2)

        initial_frame_label = tk.Label(frame, text='Initial frame:', pady=8)
        initial_frame_label.grid(column=0, row=3, sticky=tk.E)

        self.initial_frame = tk.Entry(frame, width=3)
        self.initial_frame.insert(0, '0')
        self.initial_frame.grid(column=1, row=3)
        self.initial_frame.focus()
        self.initial_frame.select_range(0, tk.END)

        buttons = tk.Frame(frame)
        buttons.grid(column=0, columnspan=2, row=4)
        cancel = tk.Button(buttons, text='Cancel', command=self.cancel)
        cancel.pack(side='left')
        save = tk.Button(buttons, text='Save & advance', command=self.save)
        save.pack(side='right')

    def handle_destroy(self, event):
        if event.widget is self:
            self.cancel()

    def cancel(self):
        self.close()

    def save(self):
        now = int(time.time())
        initial_frame = int(self.initial_frame.get() or '0')
        new_reel = Reel(now, '', 2400, 0)
        self.close(new_reel, initial_frame)


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

        frame = tk.Frame(self)
        frame.pack(fill='both')

        label = tk.Label(frame, text='Current frame:')
        label.grid(column=0, row=0, sticky=tk.E)

        minus = tk.Button(frame, text='-', command=self.minus_one, width=1)
        minus.grid(column=1, row=0)
        self.frame_entry = tk.Entry(
            frame, textvariable=self.new_current_frame, width=5)
        self.frame_entry.grid(column=2, row=0)
        plus = tk.Button(frame, text='+', command=self.plus_one, width=1)
        plus.grid(column=3, row=0)

        buttons = tk.Frame(frame)
        buttons.grid(column=0, columnspan=4, row=1)
        cancel = tk.Button(buttons, text='Cancel', command=self.cancel)
        cancel.pack(side='left')
        save = tk.Button(buttons, text='Save', command=self.save)
        save.pack(side='right')

        self.frame_entry.focus()
        self.frame_entry.icursor(tk.END)

    def minus_one(self):
        self.new_current_frame.set(self.new_current_frame.get() - 1)

    def plus_one(self):
        self.new_current_frame.set(self.new_current_frame.get() + 1)

    def handle_destroy(self, event):
        if event.widget is self:
            self.cancel()

    def cancel(self):
        self.close()

    def save(self):
        self.close(self.new_current_frame.get())


class ReelInfo(tk.Frame):
    def __init__(
        self, master, device, reel, current_frame, update_reel,
        update_current_frame, advance_frames, reel_direction=None
    ):
        tk.Frame.__init__(
            self, master,
            relief='raised',
            borderwidth=1,
            padx=8)
        self.device = device
        self.current_frame = current_frame
        self.update_reel = update_reel
        self.update_current_frame = update_current_frame
        self.advance_frames = advance_frames
        self.reel_direction = reel_direction
        self.reel_popup = None
        self.frame_override_popup = None
        self.manual_control_popup = None
        self.create_widgets()
        self.update(reel)

    def create_widgets(self):
        big_font = tkFont.Font(size=48, weight='bold')

        frame_frame = tk.Frame(self)
        manual_frame = tk.Frame(self)
        reel_frame = tk.Frame(self)

        self.frame_count_label = tk.Label(
            frame_frame, text='Current frame')
        self.frame_override_button = tk.Label(
            frame_frame,
            text='edit',
            foreground='#77C',
            cursor='pencil',
            font=tkFont.Font(size=12))
        self.frame_override_button.bind('<Button-1>', self.edit_count)
        self.current_frame_number = tk.Label(
            frame_frame,
            font=big_font,
            padx=12)

        fw_only = self.reel_direction is not None
        self.manual_fw = tk.Button(
            manual_frame, text='Step 1' if fw_only else 'Advance 1',
            command=lambda: self.handle_advance(1))
        self.manual_fw.grid(
            row=0, column=2 if fw_only else 0)

        if fw_only:
            fw_radio = tk.Radiobutton(
                manual_frame, text='advance', value='fw',
                variable=self.reel_direction)
            fw_radio.grid(row=0, column=0)

            rw_radio = tk.Radiobutton(
                manual_frame, text='reverse', value='rw',
                variable=self.reel_direction)
            rw_radio.grid(row=0, column=1)
        else:
            self.manual_bw = tk.Button(
                manual_frame, text='Reverse 1',
                command=lambda: self.handle_advance(-1))
            self.manual_bw.grid(row=0, column=1)

        self.loaded_label = tk.Label(
            reel_frame,
            font=tkFont.Font(size=12, slant='italic'),
            foreground='#777')
        self.replace_button = tk.Button(
            reel_frame, text='Change reel',
            command=self.replace_reel)

        frame_frame.grid(row=0, column=0, pady=4)
        self.frame_count_label.grid(
            row=0, column=0, ipady=0, pady=0, sticky=tk.E+tk.S)
        self.frame_override_button.grid(
            row=1, column=0, ipady=0, pady=0, sticky=tk.E+tk.N)
        self.current_frame_number.grid(row=0, column=1, rowspan=2)

        manual_frame.grid(row=1, column=0, pady=4)

        reel_frame.grid(row=2, column=0, pady=4)
        self.loaded_label.grid(row=0, column=0)
        self.replace_button.grid(row=0, column=1)

    def handle_advance(self, n):
        if (self.device == 'camera'):
            fw = self.reel_direction.get() == 'fw'
            self.advance_frames('C', n if fw else -n)
        else:
            self.advance_frames('P', n)

    def edit_count(self, *_):
        if self.frame_override_popup is not None:
            return
        self.frame_override_popup = OverrideFramePopup(
            self.device, self.current_frame, self.close_override_popup)
        self.frame_override_popup.transient(self)
        self.frame_override_button.config(state=tk.DISABLED)

    def close_override_popup(self, new_current_frame=None):
        if new_current_frame is not None:
            self.update_current_frame(new_current_frame)
        self.frame_override_popup.destroy()
        self.frame_override_popup = None
        self.frame_override_button.config(state=tk.NORMAL)

    def replace_reel(self):
        if self.reel_popup is not None:
            return
        self.reel_popup = ReplaceReelPopup(
            self.device, self.close_replace_popup)
        self.reel_popup.transient(self)
        self.replace_button.config(state=tk.DISABLED)

    def close_replace_popup(self, reel=None, initial_frame=None):
        if reel is not None:
            self.update_reel(reel)
            if initial_frame is not None and initial_frame != 0:
                self.handle_advance(initial_frame)
        self.reel_popup.destroy()
        self.reel_popup = None
        self.replace_button.config(state=tk.NORMAL)

    def update(self, reel):
        # self.description.config(text=reel.description)
        self.loaded_label.config(text='Loaded {:%b %d}'.format(
            date.fromtimestamp(reel.loaded_at)))
        self.current_frame_number.config(text=self.current_frame.get())
