# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 18:49:47 2018

@author: Ureridu
"""
from tkinter import *
import os
import json
import inspect
import time
from importlib import reload
import sys


class funkyUser():

    def __init__(self):
        if os.path.exists(os.getcwd() + '/funkPie.py'):
            try:
                global funkPie
                import funkPie
                self.openFuncs = dict(inspect.getmembers(funkPie, inspect.isfunction))
            except Exception as e:
                print(e)
                self.openFuncs = {}
        else:
            self.openFuncs = {}

        self.makePie = {}
        for name, funk in self.openFuncs.items():
            self.makePie[name] = inspect.getsource(funk)

        self.dispFig = self.__dispFig__(self)


    def getUserInputs(self):
#        f = self.__inputsFig__(self)
#        self.openFuncs.append(f)
        pass

    def __updateFuncs__(self):
        pass


    def __write__(self):
        with open(os.getcwd() + '/funkPie.py', 'w') as outfile:
            outfile.write('\n\n'.join(list(self.makePie.values())))

        global funkPie
        try:
            del sys.modules['funkPie']
        except:
            pass
#        reload(funkPie)
        import funkPie
        self.openFuncs = dict(inspect.getmembers(funkPie, inspect.isfunction))



    class __dispFig__():
        def __init__(self, super):
            self.parent = super
            self.fig = Tk()

            self.listbox = Listbox(self.fig)
            self.openB = Button(self.fig, text='Open', command = self.__open__)
            self.delB = Button(self.fig, text='Delete', command = self.__delete__)
            self.newB = Button(self.fig, text='Add Function', command = self.__addFunk__)

            self.listbox.pack()
            self.openB.pack()
            self.delB.pack()
            self.newB.pack()

            for funk in self.parent.openFuncs:
                self.listbox.insert(END, funk)

            mainloop()

        def __open__(self, new=0):
            if not new:
                if self.listbox.curselection():
                    n = list(self.parent.openFuncs.keys())[self.listbox.curselection()[0]]
                    f = inspect.getsource(self.parent.openFuncs[n])
                    f = [x[1:] for x in f.split('\n') if '\t' in x]
                    f = '\n'.join(f)
                    v = str(inspect.signature(self.parent.openFuncs[n]))[1:-1]

                else:
                    print('No Function Selected- Creating new Function')
                    new = 1

            if new:
                n = 'userFunk'
                f = 'print("test")'
                v = 'i'

#            self.listbox.delete(END)
#            time.sleep(5)
            self.inFig = self.parent.__inputsFig__(self, self.parent, n, v, f)


        def __delete__(self):
            if self.listbox.curselection():
                n = list(self.parent.openFuncs.keys())[self.listbox.curselection()[0]]
                del self.parent.makePie[n]
                self.listbox.delete(ACTIVE)

            else:
                print('Please Select Function')

            self.parent.__write__()



        def __addFunk__(self):
            self.__open__(new=1)



    class __inputsFig__():
        def __init__(self, dispFig, super, n, v, f):
            self.dispFig = dispFig
            self.parent = super
            self.fig = Tk()
            self.label1 = Label(self.fig, text='Enter Function Name')
            self.label2 = Label(self.fig, text='Enter Argument Variables to pass to Function')
            self.label3 = Label(self.fig, text='Enter Function Body')
            self.__entry1 = Entry(self.fig)
            self.__entry2 = Entry(self.fig)
            #entry3 = Entry(self.fig)

            self.__text = Text(self.fig)
            self.__entry1.insert(END, n)
            self.__entry2.insert(END, v)
            self.__text.insert(END, f)
            self.button = Button(self.fig, text='check', command = self.checkFunc)

            self.label1.pack(side=TOP)
            self.__entry1.pack(side=TOP)
            self.label2.pack()
            self.__entry2.pack()
            #entry3.pack()
            self.label3.pack()
            self.__text.pack()
            self.button.pack()

        def checkFunc(self):
            print('validating')
            self.makeFunc()
            if self.ok:
                try:
                    self.saveButton.destroy()
                except:
                    pass

                self.saveButton = Button(self.fig, text='Save Function', command = self.saveFunc)
                self.saveButton.pack()



        def saveFunc(self):
            n, v, f = self.__getter__()

            line1 = 'def ' + n + '(' + v + '):\n'
            body = f.split('\n')
            body.insert(0, '')
            self.parent.makePie[n] = line1 + '\n\t'.join(body)
            self.parent.openFuncs[n] = self.func
#            print(self.func)
            self.parent.__write__()

            self.saveButton.destroy()

            self.dispFig.listbox.delete(0, END)
            for funk in self.parent.openFuncs:
                self.dispFig.listbox.insert(END, funk)


        def __getter__(self):
            n = self.__entry1.get()
            v = self.__entry2.get()
            f = self.__text.get(1.0, END)

            return n, v, f


        def makeFunc(self):
            n, v, f = self.__getter__()
            func = ['global ' + n]
            func.append('def ' + n + '(' + v + '):')
            splitted = f.split('\n')
            for spl in splitted:
                spl = '    ' + spl
                func.append(spl)

#            func.append('    return x')

            func = '\n'.join(func)

            try:
                exec(func)
                exec(n+'(' + v + ')')
                self.func = eval(n)

                try:
                    self.warn.destroy()
                except:
                    pass


                self.ok = 1

            except Exception as e:
                self.warn = Label(self.fig, text=e)
                self.warn.pack()
                self.ok = 0

                try:
                    self.saveButton.destroy()
                except:
                    pass



i = 1

userFuncs = funkyUser()
userFuncs.getUserInputs()

