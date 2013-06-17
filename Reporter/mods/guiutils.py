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
import datetime


class Dateentry(tk.Frame):
    def __init__(self, master=None, d=datetime.date.today()):
        tk.Frame.__init__(self, master)
        self.pack()
        dd = tk.StringVar(value=d.strftime("%d"))
        mm = tk.StringVar(value=d.strftime("%m"))
        yyyy = tk.StringVar(value=d.strftime("%Y"))
        self.E_1 = tk.Entry(self, width=2, textvariable=dd)
        self.L_1 = tk.Label(self, text='-')
        self.E_2 = tk.Entry(self, width=2, textvariable=mm)
        self.L_2 = tk.Label(self, text='-')
        self.E_3 = tk.Entry(self, width=4, textvariable=yyyy)
        self.E_1.focus()
        self.E_1.bind('<Return>', func=lambda e: self.E_2.focus_set())
        self.E_2.bind('<Return>', func=lambda e: self.E_3.focus_set())
        self.E_3.bind('<Return>', func=self.getdate())
        self.E_1.grid(row=0, column=0)
        self.L_1.grid(row=0, column=1)
        self.E_2.grid(row=0, column=2)
        self.L_2.grid(row=0, column=3)
        self.E_3.grid(row=0, column=4)

    def getdate(self):
        date = datetime.date(day=int(self.E_1.get()), month=int(self.E_2.get()), year=int(self.E_3.get())).strftime("%Y-%m-%d")
        return date


if __name__ == "__main__":
    DE = Dateentry()
    DE.mainloop()
