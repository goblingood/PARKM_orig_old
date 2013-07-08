# ZCOUNTER connects guest cards to companies
# Copyright (C) 2013  AB

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import tkinter as tk
from tkinter import ttk
try:
    import mods.zcountutils as zu
except:
    import zcountutils as zu


class Zcounter(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        self.tv_counter = ttk.Treeview(self, height=28)
        self.tv_counter.grid(row=0, column=0)

        self.scrl_counter = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tv_counter.yview)
        self.scrl_counter.grid(row=0, column=1, sticky=('N', 'S'))
        self.tv_counter['yscrollcommand'] = self.scrl_counter.set

        self.tv_counter["columns"] = ("company", "current", 'total')
        self.tv_counter.column("company", anchor='w')
        self.tv_counter.column("current", width=60, anchor='center')
        self.tv_counter.column("total", width=60, anchor='center')
        self.tv_counter.heading("company", text="Company")
        self.tv_counter.heading("current", text="Current")
        self.tv_counter.heading("total", text="Total")

        self.tv_counter['show'] = 'headings'  # supress!
        self.prev_data = []
        self.init_tv_counter()
        self.refresh_tv_counter()

    def init_tv_counter(self):
        counter_data = zu.query_count()
        for i, data in enumerate(counter_data):
            counter_data = zu.query_count()
            self.tv_counter.insert('', 'end', iid=i+1, values=data)
        self.prev_data = counter_data

    def refresh_tv_counter(self):
        counter_data = zu.query_count()
        for i, data in enumerate(counter_data):
            self.tv_counter.delete(i+1)
            if data[1] > self.prev_data[i][1]:
                self.tv_counter.insert('', 'end', iid=i+1, values=data, tag=('up',))
                self.tv_counter.tag_configure('up', background='red')
            elif data[1] < self.prev_data[i][1]:
                self.tv_counter.insert('', 'end', iid=i+1, values=data, tag=('down',))
                self.tv_counter.tag_configure('down', background='green')
            else:
                self.tv_counter.insert('', 'end', iid=i+1, values=data)
        # self.prev_data = counter_data
        self.tv_counter.after(30000, self.refresh_tv_counter)


if __name__ == "__main__":
    app = Zcounter()
    app.master.title('Парковка')
    app.master.geometry('380x600+300+200')  # WxH+X+Y
    try:
        app.master.wm_iconbitmap('mods\icon.ico')
    except tk.TclError:
        pass
    app.mainloop()
