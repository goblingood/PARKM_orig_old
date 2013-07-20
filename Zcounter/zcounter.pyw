# ZCOUNTER counts busy/total
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
        self.scrl_counter.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tv_counter['yscrollcommand'] = self.scrl_counter.set

        self.tv_counter["columns"] = ("company", "current", 'total')
        self.tv_counter.column("company", anchor=tk.W)
        self.tv_counter.column("current", width=60, anchor=tk.CENTER)
        self.tv_counter.column("total", width=60, anchor=tk.CENTER)
        self.tv_counter.heading("company", text="Company")
        self.tv_counter.heading("current", text="Current")
        self.tv_counter.heading("total", text="Total")
        self.tv_counter.bind("<<TreeviewSelect>>", self.show_inpark)

        self.tv_counter['show'] = 'headings'  # supress!
        self.prev_data = []

        self.tv_inpark = ttk.Treeview(self, height=28)
        self.tv_inpark.grid(row=0, column=2)

        self.scrl_inpark = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tv_inpark.yview)
        self.scrl_inpark.grid(row=0, column=3, sticky=(tk.N, tk.S))
        self.tv_inpark['yscrollcommand'] = self.scrl_inpark.set

        self.tv_inpark["columns"] = ("card_id", "customer", 'time_entry')
        self.tv_inpark.column("card_id", width=60, anchor=tk.W)
        self.tv_inpark.column("customer", width=300, anchor=tk.W)
        self.tv_inpark.column("time_entry", width=110, anchor=tk.CENTER)
        self.tv_inpark.heading("card_id", text="Card ID")
        self.tv_inpark.heading("customer", text="Customer")
        self.tv_inpark.heading("time_entry", text="Time entry")

        self.tv_inpark['show'] = 'headings'  # supress!
        self.tv_counter_sel = None
        self.prev_data = zu.query_count()

        self.refresh_tv_counter()

    def refresh_tv_counter(self):
        counter_data = zu.query_count()
        self.tv_counter.delete(*self.tv_counter.get_children())
        for i, data in enumerate(counter_data):
            if data[1] > self.prev_data[i][1]:
                self.tv_counter.insert('', 'end', iid=i+1, values=data, tag=('up',))
                self.tv_counter.tag_configure('up', background='red')
            elif data[1] < self.prev_data[i][1]:
                self.tv_counter.insert('', 'end', iid=i+1, values=data, tag=('down',))
                self.tv_counter.tag_configure('down', background='green')
            else:
                self.tv_counter.insert('', 'end', iid=i+1, values=data)
        try:
            self.tv_counter.selection_set(self.tv_counter_sel)
        except tk.TclError:
            pass
        else:
            self.tv_counter.focus(self.tv_counter_sel)  # keep control up/down arrow button scroll after refresh
        self.prev_data = counter_data  # ####
        self.tv_counter.after(30000, self.refresh_tv_counter)

    def show_inpark(self, event=None):
        # self.tv_counter_sel = self.tv_counter.focus()  # or below
        item_no = self.tv_counter.selection()[0]  # or above
        self.tv_counter_sel = item_no  # can be improve
        company_name = self.tv_counter.item(item_no)['values'][0]
        inpark_data = zu.query_company_inpark(company_name)
        self.tv_inpark.delete(*self.tv_inpark.get_children())
        for i, data in enumerate(inpark_data):
            self.tv_inpark.insert('', 'end', iid=i+1, values=data)


if __name__ == "__main__":
    app = Zcounter()
    app.master.title('Парковка')
    app.master.geometry('870x600+300+200')  # WxH+X+Y
    try:
        app.master.wm_iconbitmap('mods\icon.ico')
    except tk.TclError:
        pass
    app.mainloop()
