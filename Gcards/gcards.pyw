# GCARDS connects guest cards to companies
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
    import mods.sqlutils as sq
except:
    import sqlutils as sq


class Gcards(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        self.lv = tk.StringVar()
        self.lbx_cards = tk.Listbox(self, width=15, height=15, selectmode=tk.EXTENDED, exportselection=False, listvariable=self.lv)
        self.lbx_cards.grid(row=0, column=0, rowspan=2)

        self.scrl_cards = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.lbx_cards.yview)
        self.scrl_cards.grid(row=0, column=1, rowspan=2, sticky=(tk.N, tk.S))

        self.cbx_curcompany = ttk.Combobox(self, width=35, values=['Непривязанные'] + sq.get_companies_list(), state='readonly')
        self.cbx_curcompany.set('Непривязанные')
        self.cbx_curcompany.bind('<<ComboboxSelected>>', self.fill_gcards_listbox)
        self.cbx_curcompany.grid(row=0, column=2, sticky=tk.N)

        self.cbx_newcompany = ttk.Combobox(self, width=35, values=['Непривязанные'] + sq.get_companies_list(), state='readonly')
        self.cbx_newcompany.set('Непривязанные')
        self.cbx_newcompany.grid(row=1, column=2, sticky=tk.N)

        self.btn_link = tk.Button(self, width=15, text='Привязать', command=self.register_gcards)
        self.btn_link.grid(row=2, column=2, padx=5, pady=5)

        # self.btn_purge = tk.Button(self, width=15, text='Привязать', command=self.register_gcards)
        # self.btn_purge.grid(row=2, column=2, padx=5, pady=5)

        self.lbl_status = tk.Label(self, text='Status...')
        self.lbl_status.grid(row=3, column=0, padx=5, columnspan=2, sticky='W')

        self.lbx_cards['yscrollcommand'] = self.scrl_cards.set
        self.fill_gcards_listbox()

    def fill_gcards_listbox(self, event=None):
        self.lv.set(tuple(sq.get_gcards_list(self.cbx_curcompany.get())))

    def register_gcards(self):
        self.btn_link.config(state=tk.DISABLED)
        self.btn_link.update_idletasks()  # ??
        gcards = [self.lbx_cards.get(i) for i in self.lbx_cards.curselection()]
        # gcards = [self.lbx_cards.get(int(i)) for i in self.lbx_cards.curselection()]  # use for old Tkinter bug
        sq.register_gcards(gcards, self.cbx_curcompany.get(), self.cbx_newcompany.get())
        self.fill_gcards_listbox()
        self.btn_link.update()  # ??
        self.btn_link.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = Gcards()
    app.master.title('Отчёты')
    app.master.geometry('380x300+300+200')  # WxH+X+Y
    try:
        app.master.wm_iconbitmap('mods\icon.ico')
    except tk.TclError:
        pass
    app.mainloop()
