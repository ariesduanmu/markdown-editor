# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2020-04-10 09:19:32
# @Last Modified by:   Li Qin
# @Last Modified time: 2020-04-10 11:09:58
from tkinter import Frame, BOTH, Tk, Text, LEFT, RIGHT, END, Menu
from tkinter import font , filedialog
from tkinter import messagebox as mbox
from markdown2 import Markdown
from tkhtmlview import HTMLLabel

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family='Helvetica', size=14)
        self.init_window()

    def init_window(self):
        self.master.title("Markdown 编辑器")
        self.pack(fill=BOTH, expand=1)

        self.inputeditor = Text(self, width="1", font=self.myfont)
        self.inputeditor.pack(fill=BOTH, expand=1, side=LEFT)

        self.outputbox = HTMLLabel(self, width="1", background="white", html="<h1>Markdown 编辑器</h1>")
        self.outputbox.pack(fill=BOTH, expand=1, side=RIGHT)
        self.outputbox.fit_height()

        self.inputeditor.bind("<<Modified>>", self.onInputChange)

        self.mainmenu = Menu(self)
        self.filemenu = Menu(self.mainmenu)
        self.filemenu.add_command(label="打开", command=self.openfile)
        self.filemenu.add_command(label="另存为", command=self.savefile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="退出", command=self.quit)
        self.mainmenu.add_cascade(label="文件", menu=self.filemenu)
        self.master.config(menu=self.mainmenu)

    def onInputChange(self, event):
        self.inputeditor.edit_modified(0)
        md2html = Markdown()
        self.outputbox.set_html(md2html.convert(self.inputeditor.get('1.0', END)))

    def openfile(self):
        openfilename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *mdown , *.markdown"),
                                                             ("Text File", "*.txt"),
                                                             ("All Files", "*.*")))
        if openfilename:
            try:
                self.inputeditor.delete(1.0, END)
                self.inputeditor.insert(END, open(openfilename, encoding='utf-8').read())
            except Exception as e:
                mbox.showerror(f"无法打开文件({openfilename})！Error:{e}")

    def savefile(self):
        filedata = self.inputeditor.get("1.0", END)
        savefilename = filedialog.asksaveasfilename(filetypes=(("Markdown File", "*.md"),
                                                              ("Text File", "*.txt")),
                                                    title="保存Markdown 文件")
        if savefilename:
            try:
                with open(savefilename, 'w', encoding='utf-8') as f:
                    f.write(filedata)
            except Exception as e:
                mbox.showerror("保存文件错误", f"文件{savefilename}保存错误！ERROR: {e}")


    def quit(self):
        self.master.quit()


root = Tk()
root.geometry("800x600")
app = Window(root)
app.mainloop()