# REPORTER connects guest cards to companies
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
from tkinter import filedialog
import datetime
try:
    import mods.reports as reports
    import mods.guiutils as guiutils
except:
    import reports as reports
    import guiutils as guiutils


class Reporter(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.btn_report = tk.Button(self, width=15, text='Выгрузить в Excel', command=self.create_report)
        self.btn_report.grid(row=0, column=0, padx=5, pady=5)
        self.btn_chdir = tk.Button(self, width=15, text='Сменить каталог', command=self.select_dir)
        self.btn_chdir.grid(row=1, column=0, padx=5, pady=5)
        self.cbx_companies = ttk.Combobox(self, width=35, values=['Все компании'] + reports.get_companies_list(), state='readonly')
        self.cbx_companies.set('Все компании')
        self.cbx_companies.grid(row=0, column=1)
        self.lbl_path = tk.Label(self, text='C:/Reports/')
        self.lbl_path.grid(row=1, column=1, sticky='W')
        self.lbl_status = tk.Label(self, text='Status...')
        self.lbl_status.grid(row=2, column=0, padx=5, columnspan=2, sticky='W')
        self.lbl_dt_from = tk.Label(self, text='С: ')
        self.lbl_dt_from.grid(row=0, column=2)
        self.lbl_dt_to = tk.Label(self, text='По:')
        self.lbl_dt_to.grid(row=1, column=2)
        self.de_dt_from = guiutils.Dateentry(self, datetime.date(day=1, month=datetime.date.today().month,
                                                                 year=datetime.date.today().year))
        self.de_dt_from.grid(row=0, column=3)
        self.de_dt_to = guiutils.Dateentry(self)
        self.de_dt_to.grid(row=1, column=3)

        self.working = False

    def select_dir(self):
        path = filedialog.askdirectory()
        if path != '':
            self.lbl_path.configure(text=path + '/')

    def create_report(self):
        if not self.working:
            self.working = True  # new dirty hack
            self.btn_report.config(state=tk.DISABLED)
            self.lbl_status.config(text='Wait...')
            self.update()
            reports.reports(self.cbx_companies.get(), self.lbl_path.cget('text'), self.cbx_companies.cget('values'), self.lbl_status,
                            self.de_dt_from.getdate(), self.de_dt_to.getdate())
            # self.update()  # some dirty hack
            self.btn_report.config(state=tk.NORMAL)
            self.lbl_status.config(text='Status...')


if __name__ == "__main__":
    app = Reporter()
    app.master.title('Отчёты')
    app.master.geometry('480x100+300+200')  # WxH+X+Y
    try:
        app.master.wm_iconbitmap('icon.ico')
    except tk.TclError:
        pass
    app.mainloop()
