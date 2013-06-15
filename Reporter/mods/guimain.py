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

        self.B_create_report = tk.Button(self, width=15, text='Выгрузить в Excel',
                                         command=lambda: reports.reports(self.C_company_list.get(), self.L_path_label.cget('text'),
                                                                         self.C_company_list.cget('values'), self.L_status,
                                                                         self.DE_date_from.getdate(), self.DE_date_to.getdate()))
        self.B_create_report.grid(row=0, column=0, padx=5, pady=5)

        self.B_change_dir = tk.Button(self, width=15, text='Сменить каталог', command=self.select_dir)
        self.B_change_dir.grid(row=1, column=0, padx=5, pady=5)

        self.C_company_list = ttk.Combobox(self, width=35, values=['Все компании'] + reports.get_companies_list(), state='readonly')
        self.C_company_list.set('Все компании')
        self.C_company_list.grid(row=0, column=1)

        self.L_path_label = tk.Label(self, text='C:/Reports/')
        self.L_path_label.grid(row=1, column=1, sticky='W')

        self.L_status = tk.Label(self, text='Status...')
        self.L_status.grid(row=2, column=0, padx=5, columnspan=2, sticky='W')

        self.L_date_from = tk.Label(self, text='С: ')
        self.L_date_from.grid(row=0, column=2)

        self.L_date_to = tk.Label(self, text='По:')
        self.DE_date_from = guiutils.Dateentry(self, datetime.date(day=1, month=datetime.date.today().month,
                                                                   year=datetime.date.today().year))
        self.DE_date_from.grid(row=0, column=3)

        self.L_date_to.grid(row=1, column=2)
        self.DE_date_to = guiutils.Dateentry(self)
        self.DE_date_to.grid(row=1, column=3)

    def select_dir(self):
        path = filedialog.askdirectory()
        if path != '':
            self.L_path_label.configure(text=path + '/')


if __name__ == "__main__":
    app = Reporter()
    app.master.title('Отчёты')
    app.master.geometry('480x100+300+200')  # WxH+X+Y
    try:
        app.master.wm_iconbitmap('icon.ico')
    except tk.TclError:
        pass
    app.mainloop()
