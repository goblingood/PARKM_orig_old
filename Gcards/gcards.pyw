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

        self.LB_cards = tk.Listbox(self, width=15, height=15, selectmode=tk.EXTENDED, exportselection=False, listvariable=self.lv)
        self.LB_cards.grid(row=0, column=0, rowspan=2)

        self.S_cards = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.LB_cards.yview)
        self.S_cards.grid(row=0, column=1, rowspan=2, sticky=(tk.N, tk.S))

        self.LB_cards['yscrollcommand'] = self.S_cards.set

        self.C_company_list_cur = ttk.Combobox(self, width=35, values=['Непривязанные'] + sq.get_companies_list(), state='readonly')
        self.C_company_list_cur.set('Непривязанные')
        self.C_company_list_cur.grid(row=0, column=2, sticky=tk.N)

        self.B_gcards_link = tk.Button(self, width=15, text='Привязать',
                                       command=self.register_gcards)
        self.C_company_list_new = ttk.Combobox(self, width=35, values=['Непривязанные'] + sq.get_companies_list(), state='readonly')
        self.C_company_list_new.set('Непривязанные')
        self.C_company_list_new.grid(row=1, column=2, sticky=tk.N)

        self.B_gcards_link.grid(row=2, column=2, padx=5, pady=5)

        self.C_company_list_cur.bind('<<ComboboxSelected>>', self.fill_gcards_listbox)

        self.L_status = tk.Label(self, text='Status...')
        self.L_status.grid(row=3, column=0, padx=5, columnspan=2, sticky='W')

        self.fill_gcards_listbox()

    def fill_gcards_listbox(self, event=None):
        self.lv.set(tuple(sq.get_gcards_list(self.C_company_list_cur.get())))

    def register_gcards(self):
        self.B_gcards_link.config(state=tk.DISABLED)
        gcards = [self.LB_cards.get(int(i)) for i in self.LB_cards.curselection()]
        sq.register_gcards(gcards, self.C_company_list_cur.get(), self.C_company_list_new.get())
        self.fill_gcards_listbox()
        self.B_gcards_link.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = Gcards()
    app.master.title('Отчёты')
    app.master.geometry('380x300+300+200')  # WxH+X+Y
    try:
        app.master.wm_iconbitmap('mods\icon.ico')
    except tk.TclError:
        pass
    app.mainloop()
