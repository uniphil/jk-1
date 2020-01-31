import Tkinter as tk
import time

LOG_TTL = 5


class StatusBar(tk.Frame):
    def __init__(self, master, latest_update, on_cancel, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.last_update_message = latest_update
        self.cancel = on_cancel
        self.last_update_time = time.time()
        self.program_length = 0

        # FIXME
        # self.progress_bar = tk.Progressbar(
        #     self, mode='determinate')
        # self.progress_bar.grid(row=0, column=0, padx=6)

        self.cancel_button = tk.Button(
            self, text='Cancel', command=self.cancel)

        tk.Label(self, textvariable=latest_update).grid(
            row=0, column=2, sticky=tk.W)
        self.last_update_message.trace('w', self.handle_log_update)

    def handle_log_update(self, *args):
        self.last_update_time = time.time()
        self.after(LOG_TTL * 1000 + 200, self.maybe_clear_update)

    def maybe_clear_update(self, *args):
        dt = time.time() - self.last_update_time
        if dt > LOG_TTL:
            self.last_update_message.set('')

    def define_program(self, n):
        self.program_length = n
        # self.progress_bar.config(maximum=n, value=0)  # FIXME
        self.cancel_button.grid(row=0, column=1)

    def update_program(self, n_remaining):
        # self.progress_bar.config(value=self.program_length - n_remaining + 1)
        pass  # FIXME

    def update_program_step(self, by_n):
        # self.progress_bar.step(by_n)
        pass  # FIXME

    def end_program(self):
        # self.progress_bar.config(value=0)
        self.cancel_button.grid_forget()
