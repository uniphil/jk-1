import Tkinter as tk
import time
import ttk

from ..reel import Reel


class ReplaceReelPopup(tk.Toplevel):
    def __init__(self, device, close):
        tk.Toplevel.__init__(self)
        self.close = close
        self.title('Replace {} reel...'.format(device))
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

        minus = ttk.Button(frame, text='-', command=self.minus_one, width=1)
        minus.grid(column=1, row=0)
        self.frame_entry = ttk.Entry(
            frame, textvariable=self.new_current_frame, width=5)
        self.frame_entry.grid(column=2, row=0)
        plus = ttk.Button(frame, text='+', command=self.plus_one, width=1)
        plus.grid(column=3, row=0)

        buttons = ttk.Frame(frame)
        buttons.grid(column=0, columnspan=4, row=1)
        cancel = ttk.Button(buttons, text='Cancel', command=self.cancel)
        cancel.pack(side='left')
        save = ttk.Button(buttons, text='Save', command=self.save)
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


class ManualControlPopup(tk.Toplevel):
    def __init__(self, device, current_frame, advance, close):
        tk.Toplevel.__init__(self)
        self.current_frame = current_frame
        self.title('Manual control: {}'.format(device))

        self.advance = advance
        self.close = close

        self.reverse = tk.BooleanVar()
        self.reverse.set(False)

        self.frames_to_advance = tk.IntVar()
        self.frames_to_advance.set(1)

        self.reverse.trace('w', self.handle_set_frames)
        self.current_frame_trace_id = self.current_frame.trace_variable(
            'w', self.handle_current_frame)
        self.bind('<Destroy>', self.handle_destroy)
        self.bind('<Escape>', lambda _: self.done())

        frame = ttk.Frame(self)
        frame.pack(fill='both')

        self.current_frame_label = ttk.Label(
            frame, text='Current frame: {}'.format(self.current_frame.get()))
        self.current_frame_label.grid(column=0, row=0, sticky=tk.E)

        reverse_option = ttk.Checkbutton(
            frame, text='Reverse', variable=self.reverse)
        reverse_option.grid(column=1, row=0)

        frame_num_entry = ttk.Entry(
            frame, textvariable=self.frames_to_advance, width=8)
        frame_num_entry.bind('<KeyRelease>', self.handle_set_frames)
        frame_num_entry.bind('<FocusOut>', self.handle_set_frames)
        frame_num_entry.grid(column=0, row=1)

        self.advance_button = ttk.Button(
            frame,
            text='Advance {} frames'.format(self.frames_to_advance.get()),
            command=self.handle_advance)
        self.advance_button.grid(column=0, columnspan=2, row=2)

        buttons = ttk.Frame(frame)
        buttons.grid(column=0, columnspan=4, row=4)

        done = ttk.Button(buttons, text='Done', command=self.done)
        done.pack(side='bottom')

    def get_frames(self):
        n = self.frames_to_advance.get()
        if self.reverse.get():
            n *= -1
        return n

    def handle_advance(self):
        self.advance(self.get_frames())

    def handle_current_frame(self, *args):
        if self.current_frame is None:
            print 'waaaaat'
        else:
            self.current_frame_label.config(
                text='Current frame: {}'.format(self.current_frame.get()))

    def handle_set_frames(self, *args):
        action = 'Reverse' if self.reverse.get() else 'Advance'
        self.advance_button.config(
            text='{} {} frames'.format(action, self.frames_to_advance.get()))

    def handle_destroy(self, event):
        if event.widget is self:
            self.current_frame.trace_vdelete('w', self.current_frame_trace_id)
            self.done()

    def done(self):
        self.close()


class ReelInfo(ttk.Frame):
    def __init__(
        self, master, device, reel, current_frame, update_reel,
        update_current_frame, advance_frames,
    ):
        ttk.Frame.__init__(self, master, relief='solid', borderwidth=2)
        self.device = device
        self.current_frame = current_frame
        self.update_reel = update_reel
        self.update_current_frame = update_current_frame
        self.advance_frames = advance_frames
        self.reel_popup = None
        self.frame_override_popup = None
        self.manual_control_popup = None
        self.create_widgets()
        self.update(reel)

    def create_widgets(self):
        info_frame = ttk.Frame(self)
        button_frame = ttk.Frame(self)
        manual_frame = ttk.Frame(self)

        self.description = ttk.Label(info_frame)
        self.loaded_label = ttk.Label(info_frame)
        self.film_frame = ttk.Label(info_frame)

        self.frame_override_button = ttk.Button(
            button_frame, text='Edit frame count', command=self.edit_count)
        self.replace_button = ttk.Button(
            button_frame, text='Replace reel', command=self.replace_reel)

        self.manual_button = ttk.Button(
            manual_frame, text='Manual control', command=self.control_manually)

        info_frame.grid(row=0, column=0, sticky=tk.W, padx=8, pady=6)
        button_frame.grid(row=1, column=0, sticky=tk.W, padx=4, pady=3)
        manual_frame.grid(row=2, column=0, columnspan=2)

        self.description.grid(row=0, column=0, sticky=tk.W)
        self.loaded_label.grid(row=1, column=0, sticky=tk.W)
        self.film_frame.grid(row=2, column=0, sticky=tk.W)

        self.frame_override_button.grid(row=0, column=0)
        self.replace_button.grid(row=0, column=1)

        self.manual_button.grid()

    def handle_advance(self, n):
        if (self.device == 'camera'):
            self.advance_frames('C', n)
        else:
            self.advance_frames('P', n)

    def edit_count(self):
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

    def close_replace_popup(self, reel):
        if reel is not None:
            self.update_reel(reel)
        self.reel_popup.destroy()
        self.reel_popup = None
        self.replace_button.config(state=tk.NORMAL)

    def control_manually(self):
        if self.manual_control_popup is not None:
            return
        self.manual_control_popup = ManualControlPopup(
            self.device, self.current_frame, self.handle_advance,
            self.close_manual_control)
        self.manual_control_popup.transient(self)
        self.manual_button.config(state=tk.DISABLED)

    def close_manual_control(self):
        if self.manual_control_popup is None:
            return
        self.manual_control_popup.destroy()
        self.manual_control_popup = None
        self.manual_button.config(state=tk.NORMAL)

    def update(self, reel):
        self.description.config(text='Reel: {}'.format(reel.description))
        self.loaded_label.config(
            text='Loaded: {}'.format(time.ctime(reel.loaded_at)))
        self.film_frame.config(text='Frame: {} of {} ({:.1%})'.format(
            self.current_frame.get(), reel.total_frames,
            self.current_frame.get() / float(reel.total_frames)))
