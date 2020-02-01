import Tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        tk.Frame.__init__(self, container, *args, **kwargs)
        child_kwargs = {}
        if 'background' in kwargs:
            child_kwargs['background'] = kwargs['background']

        self.canvas = tk.Canvas(self, highlightthickness=0, **child_kwargs)
        self.scrollbar = tk.Scrollbar(
            self, orient='vertical', command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, **child_kwargs)

        self.scrollable_frame.bind_all('<Configure>', self.handle_configure)

        self.canvas.bind_all(
            '<MouseWheel>', self.scroll)

        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(
            yscrollincrement=4,
            yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y', padx=(8, 0))

        self.size_contents()

    def scroll(self, evt):
        self.size_contents()
        if self.scrollable_frame.winfo_height() < self.canvas.winfo_height():
            self.canvas.yview(tk.MOVETO, 0)
            return
        self.canvas.yview(tk.SCROLL, evt.delta, tk.UNITS)

    def size_contents(self, *_):
        height = 2  # hack for top border
        for child in self.scrollable_frame.grid_slaves():
            pady = sum(
                int(n) for n in child.grid_info().get('pady', '').split(' '))
            height += child.winfo_height() + pady

        self.canvas.itemconfigure(
            self.canvas_frame,
            width=self.canvas.winfo_width(),
            height=height)

    def handle_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.size_contents()
