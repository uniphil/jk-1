import time
import ttk


class StatusBar(ttk.Frame):
    def __init__(self, master, latest_update):
        ttk.Frame.__init__(self, master)
        self.last_update_message = latest_update
        self.last_update_time = time.time()
        ttk.Label(self, textvariable=latest_update).pack()
        self.last_update_message.trace('w', self.handle_log_update)

    def handle_log_update(self, *args):
        self.last_update_time = time.time()
        self.after(3000, self.maybe_clear_update)

    def maybe_clear_update(self, *args):
        dt = time.time() - self.last_update_time
        if dt > 2.8:
            self.last_update_message.set('')
