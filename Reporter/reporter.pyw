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
