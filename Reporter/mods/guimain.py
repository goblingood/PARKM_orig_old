# REPORTER create reports
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
import tkinter.messagebox as messagebox
import tkinter.scrolledtext
from tkinter import ttk
from tkinter import filedialog
import threading
import queue
import datetime
try:
    import mods.reports as reports
    import mods.guiutils as guiutils
    import mods.exthreading as exthreading
except:
    import reports as reports
    import guiutils as guiutils
    import exthreading as exthreading


class Reporter(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.protocol('WM_DELETE_WINDOW', self.on_close)
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
        self.info_window = tkinter.scrolledtext.ScrolledText(self, height=5, width=55, wrap='word', state='disabled')
        self.info_window.grid(row=3, column=0, columnspan=4)

        self.textinfo = queue.Queue()
        self.exceptioninfo = queue.Queue()
        self.working = threading.Event()
        self.thr = None

    def on_close(self):
        if self.working.is_set():
            self.after(1000, self.on_close)
        else:
            self.master.quit()

    def select_dir(self):
        path = filedialog.askdirectory()
        if path != '':
            self.lbl_path.configure(text=path + '/')

    def create_report(self):
        self.btn_report.config(state='disabled')
        self.lbl_status.config(text='Wait...')
        self.working.set()
        try:
            self.thr = exthreading.Exthread(target=reports.reports,
                                            args=(self.cbx_companies.get(), self.lbl_path.cget('text'), self.cbx_companies.cget('values'),
                                            self.lbl_status, self.de_dt_from.getdate(), self.de_dt_to.getdate(), self.textinfo),
                                            daemon=False, exceptioninfo=self.exceptioninfo)
            self.thr.start()
        except ValueError as err:
            messagebox.showerror('ERROR', err)
        finally:
            self.check_working()

    def check_working(self):
        if self.thr is not None and self.thr.is_alive():

            self.info_window.config(state='normal')
            try:
                self.info_window.insert('end', self.textinfo.get(block=False))
            except queue.Empty:
                pass
            else:
                self.info_window.see('end')
                self.textinfo.task_done()
            self.info_window.config(state='disabled')

            try:
                messagebox.showerror('ERROR', self.exceptioninfo.get(block=False))
            except queue.Empty:
                pass
            else:
                self.exceptioninfo.task_done()

            self.after(100, self.check_working)
        else:
            self.btn_report.config(state=tk.NORMAL)
            self.lbl_status.config(text='Status...')
            self.working.clear()


if __name__ == "__main__":
    app = Reporter()
    app.master.title('Отчёты')
    app.master.geometry('480x190+300+200')  # WxH+X+Y
    try:
        app.master.wm_iconbitmap('icon.ico')
    except tk.TclError:
        pass
    app.mainloop()
