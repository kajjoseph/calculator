import tkinter as tk
from tkinter.constants import *


class DecimalButton(tk.Button):
    '''
    Button that adds a decimal to the string stored in Calculator.display_data
    '''
    def __init__(self, master):
        
        self.master = master
        tk.Button.__init__(self, master, text='.', command=self.press)

    def press(self):

        if self.master.answered:
            self.master.display_data = '0.'
            self.master.update_display()
            self.master.answered = False
            return
        for i in self.master.display_data[::-1]:
            if i == '.':
                return
            if i in OperatorButton.operators:
                break
        self.master.display_data += '.'
        self.master.update_display()


class NumberButton(tk.Button):
    '''
    Button that adds the assigned number to the string stored in Calculator.display_data
    '''
    def __init__(self, master, number):
        
        self.master = master
        self.number = number
        tk.Button.__init__(self, master, text=number, command=self.press)

    def press(self):
        
        if self.master.display_data == '0' or self.master.answered:
            self.master.display_data = self.number
            self.master.update_display()
            self.master.answered = False
        else:
            self.master.display_data += self.number
            self.master.update_display()


class OperatorButton(tk.Button):
    '''
    Button that adds the assigned operator to the string stored in Calculator.display_data
    '''
    operators = ['+', '-', '*', '/']

    def __init__(self, master, operator):
        
        self.master = master
        self.operator = operator
        tk.Button.__init__(self, master, text=operator, command=self.press)

    def press(self):
        
        if self.master.display_data[-1] not in OperatorButton.operators:
            if self.master.display_data[-1] == '.':
                self.master.display_data += '0'
            self.master.display_data += self.operator
            self.master.update_display()


class EqualButton(tk.Button):
    '''
    Button that evaluates the string stored in Calculator.display_data
    '''
    def __init__(self, master):
        
        self.master = master
        tk.Button.__init__(self, master, text='=', command=self.press)

    def press(self):

        if not self.master.answered:
            if self.master.display_data[-1] == '.':
                self.master.display_data += '0'
                self.master.update_display()
            try:
                self.master.display_data = str(eval(self.master.display_data))
                self.master.update_display()
                
            except Exception as exc:
                self.master.display_data = 'ERROR!'
                print(exc)
                self.master.update_display()
            self.master.answered = True


class Calculator(tk.Frame):
    '''
    Frame for storing and representing buttons and the display
    '''
    def __init__(self, master):
        
        self.master = master
        tk.Frame.__init__(self, master)

        self.answered = False

        # Initialize display variables
        self.display_data = '0'
        self.display_var = tk.StringVar()
        self.update_display()
        self.display = tk.Label(self, textvar=self.display_var, relief=SUNKEN)
        self.display.grid(row=0, column=0, columnspan=4)
        
        # Place number buttons
        row = 1
        col = 0
        for i in range(1, 10):
            NumberButton(self, str(i)).grid(row=row, column=col)
            col += 1
            if col == 3:
                row += 1
                col = 0
        NumberButton(self, '0').grid(row=row, column=col+1)
        EqualButton(self).grid(row=row, column=col+2)
        DecimalButton(self).grid(row=row, column=0)

        # Place operator buttons
        row = 1
        for i in OperatorButton.operators:
            OperatorButton(self, i).grid(row=row, column=4)
            row += 1
        
    def update_display(self):
        self.display_var.set(self.display_data)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Calculator')
    root.config(width=500)
    calc = Calculator(root)
    calc.pack()
    root.mainloop()
