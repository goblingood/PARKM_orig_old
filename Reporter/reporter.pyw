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
import mods.guimain as guimain


app = guimain.Reporter()
app.master.title('Отчёты')
app.master.geometry('480x100+300+200')  # WxH+X+Y
app.master.resizable(False, False)
try:
    app.master.wm_iconbitmap('mods\icon.ico')
except tk.TclError:
    pass

app.mainloop()
