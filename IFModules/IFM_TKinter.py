# -*- coding: utf-8 -*-
import tkinter, time, os

class Interface():
  def __init__(self, API):
    self.API = API

  def FromUser(self, event=None):
    w_text = self.Text_In.get('1.0', tkinter.END)
    #print 'write', type(w_text)
    #if event == None: return
    self.Text_In.delete('1.0', tkinter.END)
    self.Text_Out.insert(tkinter.END, u'I said: ' + w_text + u'\n')
    self.API.write_text(self, w_text)

  def to_IF(self, r_text):
    self.Text_Out.insert(tkinter.END, u'ManSPy: ' + r_text + u'\n')

  def init(self):
    self.root1 = tkinter.Tk()

    self.Text_Out = tkinter.Text(self.root1, width=70, height=30, font='Arial 11',wrap=tkinter.WORD)
    self.Text_Out.pack()

    self.Text_In = tkinter.Text(self.root1, width=70, height=3, font='Arial 11',wrap=tkinter.WORD)
    #self.Text_In.bind("<Enter>", FromUser)
    self.Text_In.pack()

    Button_Send = tkinter.Button(self.root1, text=u'Отправить', command=self.FromUser)
    Button_Send.pack()

    self.root1.mainloop()
