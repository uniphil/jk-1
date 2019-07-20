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
        self.frame_entry.focus()
        plus = ttk.Button(frame, text='+', command=self.plus_one, width=1)
        plus.grid(column=3, row=0)

        buttons = ttk.Frame(frame)
        buttons.grid(column=0, columnspan=4, row=1)
        cancel = ttk.Button(buttons, text='Cancel', command=self.cancel)
        cancel.pack(side='left')
        save = ttk.Button(buttons, text='Save', command=self.save)
        save.pack(side='right')

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
        self.current_frame.set(self.new_current_frame.get())
        self.close()


class ReelInfo(ttk.Frame):
    def __init__(self, master, device, reel, current_frame, update_reel):
        ttk.Frame.__init__(self, master, relief='solid', borderwidth=2)
        self.device = device
        self.current_frame = current_frame
        self.update_reel = update_reel
        self.reel_popup = None
        self.frame_override_popup = None
        self.create_widgets()
        self.update(reel)

    def create_widgets(self):
        reel_label = ttk.Label(self, text='Reel:')
        reel_label.grid(column=0, row=0)

        reel_frame = ttk.Frame(self)
        reel_frame.grid(column=1, row=0, sticky=tk.W)
        self.description = ttk.Label(reel_frame)
        self.description.pack(anchor=tk.W)

        self.loaded = ttk.Label(reel_frame)
        self.loaded.pack(anchor=tk.W)

        self.replace_button = ttk.Button(
            reel_frame, text='replace', command=self.replace_reel)
        self.replace_button.pack(anchor=tk.W)

        frame_label = ttk.Label(self, text='Frame:')
        frame_label.grid(column=0, row=1)

        count = ttk.Frame(self)
        count.grid(column=1, row=1, sticky=tk.W)
        self.film_frame = ttk.Label(count)
        self.film_frame.pack(anchor=tk.W)
        self.frame_override_button = ttk.Button(
            count, text='override', command=self.edit_count)
        self.frame_override_button.pack(anchor=tk.W)

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

    def update(self, reel):
        self.description.config(text=reel.description)
        self.loaded.config(text=time.ctime(reel.loaded_at))
        self.film_frame.config(text='{} (of {})'.format(
            reel.current_frame, reel.total_frames))
