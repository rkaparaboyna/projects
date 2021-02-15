import tkinter as tk
import math


class Calculator:

    def __init__(self):
        self.operations = []
        self.digits = []
        self.value = 0
        self.error = False
        self.is_decimal = False
        self.continuing = False
        self.num1_typed, self.num2_typed = False, False
        self.operation_selected = -1
        self.decimal_place = 0.1
        self.window = tk.Tk()
        title = tk.Label(text="Calculator", fg="blue")
        title.grid(columnspan=3)
        self.display = tk.Label(text="0")
        self.display.grid(columnspan=10)
        self.create_buttons()
        self.decimal = tk.Button(text=".", fg="black", width=3, height=3, command=self.apply_decimal)
        self.decimal.grid(row=3, column=8)
        self.clear = tk.Button(text="AC", fg="black", width=3, height=3, command=self.reset)
        self.clear.grid(row=2, column=9)
        self.equals = tk.Button(text="=", fg="black", width=3, height=3, command=self.apply_operation)
        self.equals.grid(row=3, column=9)
        self.exit = tk.Button(text="Exit", fg="red", command=self.turn_off)
        self.exit.grid(columnspan=3)
        self.window.mainloop()

    def create_buttons(self):
        '''Creates operation and digit buttons'''
        plus = tk.Button(text="+", width=3, height=3, fg="gray", command=lambda index=0: self.select(index))
        plus.grid(row=2, column=0)
        self.operations.append(plus)
        minus = tk.Button(text="-", width=3, height=3, fg="gray", command=lambda index=1: self.select(index))
        minus.grid(row=2, column=1)
        self.operations.append(minus)
        multiply = tk.Button(text="×", width=3, height=3, fg="gray", command=lambda index=2: self.select(index))
        multiply.grid(row=3, column=0)
        self.operations.append(multiply)
        divide = tk.Button(text="÷", width=3, height=3, fg="gray", command=lambda index=3: self.select(index))
        divide.grid(row=3, column=1)
        self.operations.append(divide)
        power = tk.Button(text="^", width=3, height=3, fg="gray", command=lambda index=4: self.select(index))
        power.grid(row=2, column=2)
        self.operations.append(power)
        logarithm = tk.Button(text="log", width=3, height=3, fg="gray", command=lambda index=5: self.select(index))
        logarithm.grid(row=3, column=2)
        self.operations.append(logarithm)
        r, c = 10, 0
        for i in range(10):
            digit = tk.Button(text=str(i), width=3, height=3, command=lambda index=i: self.pick(index))
            digit.grid(row=r//5, column=c+3)
            c = (c + 1) % 5
            r += 1
            self.digits.append(digit)
        negative = tk.Button(text="+/-", width=3, height=3, fg="black", command=self.change_sign)
        negative.grid(row=2, column=8)
        self.operations.append(negative)

    def turn_off(self):
        '''Closes calculator'''
        self.window.destroy()

    def apply_decimal(self):
        '''Indicates that the current number contains a decimal'''
        self.is_decimal = True

    def change_sign(self):
        '''Changes the sign of the current number'''
        current = float(self.display.cget('text'))
        current *= -1
        self.display.config(text=str(current))

    def reset(self):
        '''Resets the calculator'''
        self.error = False
        self.continuing = False
        self.is_decimal = False
        self.value = 0
        self.decimal_place = 0.1
        self.num1_typed, self.num2_typed = False, False
        self.display.config(text="0")

    def apply_operation(self):
        '''Applies the selected operation'''
        if self.operation_selected < 0 or not self.num2_typed:
            return
        current = float(self.display.cget('text'))
        if self.operation_selected == 0:
            self.value += current
        if self.operation_selected == 1:
            self.value -= current
        if self.operation_selected == 2:
            self.value *= current
        if self.operation_selected == 3:
            if current == 0:
                self.error = True
                self.value = "Error"
            else:
                self.value /= current
        if self.operation_selected == 4:
            self.value **= current
        if self.operation_selected == 5:
            if self.value <= 0 or current <= 0:
                self.error = True
                self.value = "Error"
            else:
                self.value = math.log(self.value, current)
        self.display.config(text=str(self.value))
        self.deselect()
        self.is_decimal = False
        self.decimal_place = 0.1
        self.num2_typed = False
        self.continuing = True

    def select(self, index):
        '''Selects the specified operator'''
        if self.error:
            return
        if self.num2_typed:
            self.apply_operation()
        if self.num1_typed:
            o = self.operations[index]
            o.config(fg="black")
            self.operation_selected = index
            self.value = float(self.display.cget('text'))
            self.is_decimal = False
            self.decimal_place = 0.1
            self.display.config(text="0")

    def pick(self, index):
        '''Updates the number being chosen'''
        if self.error:
            return
        if self.operation_selected < 0 and self.continuing:
            self.value = 0
            self.continuing = False
            self.display.config(text="0")
        num = float(self.display.cget('text'))
        if self.is_decimal:
            num = num + index * self.decimal_place
            self.decimal_place /= 10
        else:
            num = num * 10 + index
        self.display.config(text=str(num))
        if not self.num1_typed:
            self.num1_typed = True
        elif not self.num2_typed and self.operation_selected >= 0:
            self.num2_typed = True

    def deselect(self):
        '''Deselects the specified operator'''
        o = self.operations[self.operation_selected]
        o.config(fg="gray")
        self.operation_selected = -1


Calculator()
