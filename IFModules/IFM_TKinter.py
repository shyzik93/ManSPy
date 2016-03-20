# -*- coding: utf-8 -*-
import Tkinter, time, os

IFName = API = None

class Interface():
  def __init__(self, API):
    self.API = API

  def FromUser(self, event=None):
    w_text = self.Text_In.get('1.0', Tkinter.END)
    #print 'write', type(w_text)
    #if event == None: return
    self.API.write_text(IFName, w_text)
    self.Text_In.delete('1.0', Tkinter.END)
    self.Text_Out.insert(Tkinter.END, u'I said: ' + w_text + u'\n')
    self.root1.after(50, self.ToUser)

  def ToUser(self):
    r_text = self.API.read_text(IFName, 0)
    #if r_text: print 'read', type(r_text)
    if r_text:
      self.Text_Out.insert(Tkinter.END, u'ManSPy: ' + r_text + u'\n')
      time.sleep(1)
    self.root1.after(50, self.ToUser)

  def init(self):
    self.root1 = Tkinter.Tk()

    self.Text_Out = Tkinter.Text(self.root1, width=70, height=30, font='Arial 11',wrap=Tkinter.WORD)
    self.Text_Out.pack()

    self.Text_In = Tkinter.Text(self.root1, width=70, height=3, font='Arial 11',wrap=Tkinter.WORD)
    #self.Text_In.bind("<Enter>", FromUser)
    self.Text_In.pack()

    Button_Send = Tkinter.Button(self.root1, text=u'Отправить', command=self.FromUser)
    Button_Send.pack()

    self.root1.after(50, self.ToUser)
    self.root1.mainloop()
