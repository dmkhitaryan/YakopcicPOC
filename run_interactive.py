import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from functions import *


class TemperatureConverter:
    @staticmethod
    def fahrenheit_to_celsius(f):
        return (f - 32) * 5 / 9


class ConverterFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # field options
        self.counter = 0
        self.inputVs = {}
        options = {'padx': 5, 'pady': 5}
        options_entry = {'padx': 1, 'pady': 1}

        # Labels for input fields
        self.temperature_label1 = ttk.Label(self, text='t_rise')
        self.temperature_label1.grid(column=0, row=0, sticky=tk.W, **options)

        self.temperature_label2 = ttk.Label(self, text='t_on')
        self.temperature_label2.grid(column=1, row=0, sticky=tk.W, **options)

        self.temperature_label3 = ttk.Label(self, text='t_fall')
        self.temperature_label3.grid(column=2, row=0, sticky=tk.W, **options)

        self.temperature_label4 = ttk.Label(self, text='t_off')
        self.temperature_label4.grid(column=3, row=0, sticky=tk.W, **options)

        self.temperature_label5 = ttk.Label(self, text='V_on')
        self.temperature_label5.grid(column=4, row=0, sticky=tk.W, **options)

        self.temperature_label6 = ttk.Label(self, text='V_off')
        self.temperature_label6.grid(column=5, row=0, sticky=tk.W, **options)

        self.temperature_label7 = ttk.Label(self, text='n_cycles')
        self.temperature_label7.grid(column=6, row=0, sticky=tk.W, **options)

        # ---
        # Entry fields for the respective variables
        # ---
        self.t_rise = tk.DoubleVar()
        self.temperature_entry1 = ttk.Entry(self, textvariable=self.t_rise, width=5)
        self.temperature_entry1.grid(column=0, row=1, **options_entry)

        self.t_on = tk.DoubleVar()
        self.temperature_entry2 = ttk.Entry(self, textvariable=self.t_on, width=5)
        self.temperature_entry2.grid(column=1, row=1, **options_entry)

        self.t_fall = tk.DoubleVar()
        self.temperature_entry3 = ttk.Entry(self, textvariable=self.t_fall, width=5)
        self.temperature_entry3.grid(column=2, row=1, **options_entry)

        self.t_off = tk.DoubleVar()
        self.temperature_entry4 = ttk.Entry(self, textvariable=self.t_off, width=5)
        self.temperature_entry4.grid(column=3, row=1, **options_entry)

        self.V_on = tk.DoubleVar()
        self.temperature_entry5 = ttk.Entry(self, textvariable=self.V_on, width=5)
        self.temperature_entry5.grid(column=4, row=1, **options_entry)

        self.V_off = tk.DoubleVar()
        self.temperature_entry6 = ttk.Entry(self, textvariable=self.V_off, width=5)
        self.temperature_entry6.grid(column=5, row=1, **options_entry)

        self.n_cycles = tk.IntVar()
        self.temperature_entry7 = ttk.Entry(self, textvariable=self.n_cycles, width=5)
        self.temperature_entry7.grid(column=6, row=1, **options_entry)

        # ---
        # Implements the two buttons. First adds voltage pulses into dict, Second plots the results.
        # ---

        self.convert_button = ttk.Button(self, text='Add Wave')
        self.convert_button['command'] = self.convert
        self.convert_button.grid(column=7, row=1, sticky=tk.W, **options_entry)

        self.convert_button = ttk.Button(self, text='Plot Voltage')
        self.convert_button['command'] = self.interactive_iv
        self.convert_button.grid(column=8, row=1, sticky=tk.W, **options_entry)

        # ---
        # Results
        # ---
        self.result_label = ttk.Label(self)
        self.result_label.grid(row=2, columnspan=6, **options)

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def convert(self):
        """  Handle button click event
        """
        try:
            # Dictionary containing tk.Entry objects instead of actual values
            # This is converted into appropriate dictionary later
            preinputV = {'t_rise': self.temperature_entry1.get(),
                         't_on': self.temperature_entry2.get(),
                         't_fall': self.temperature_entry3.get(),
                         't_off': self.temperature_entry4.get(),
                         'V_on': self.temperature_entry5.get(),
                         'V_off': self.temperature_entry6.get(),
                         'n_cycles': self.temperature_entry7.get()}


            self.inputVs[self.counter] = preinputV
            self.counter += 1
            result = f'A voltage wave has been added'
            print(self.counter)
            print(self.inputVs)
            self.result_label.config(text=result)
        except ValueError:
            showerror(title='Error', message="error")

    def interactive_iv(self):
        iptVs = self.inputVs
        print(iptVs)
        dt = 10e-3
        t = 0
        frequency = int(1 / dt)
        v_total = np.array([0])
        for iptV in iptVs.values():
            print("Printing:", iptV)
            for j in range(0, int(iptV['n_cycles'])):
                t, v_total = interactive_generate(iptV, frequency, t)

        time = np.arange(0, t, dt)
        plt.plot(time, v_total)
        plt.show()
        return time, v_total


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Temperature Converter')
        self.geometry('500x250')
        self.resizable(False, False)


if __name__ == "__main__":
    app = App()
    ConverterFrame(app)
    app.mainloop()
