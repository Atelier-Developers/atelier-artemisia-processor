import tkinter as tk

reg_name = {
    '$zero': 1,
    '$at': 1,
    '$v': 2,
    '$a': 4,
    '$t': 8,
    '$s': 8,
    '$tt': 2,
    '$k': 2,
    '$gp': 1,
    '$sp': 1,
    '$fp': 1,
    '$ra': 1
}


def reg_init():
    registers = {}
    n = 0
    for key, value in reg_name.items():
        for i in range(value):
            b = bin(n)[2:].zfill(5)
            if key == "$zero":
                registers[f"{key}"] = b
            elif key == "$tt":
                registers[f"$t{i + 8}"] = b
            else:
                registers[f"{key}{i}"] = b
            n += 1
    return registers


registers = reg_init()


class PipelineGUI:
    def __init__(self):
        self.window = tk.Tk()
        topframe = tk.Frame(master=self.window, width=200, height=250)
        topframe.pack(fill=tk.BOTH, expand=True)

        self.reg_frame = tk.Frame(master=topframe, height=200, width=250)
        self.reg_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.history_frame = tk.Frame(master=topframe, width=50, bg='yellow')
        self.history_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.option_frame = tk.Frame(master=self.window, height=50, bg='blue')
        self.option_frame.pack(fill=tk.BOTH, expand=True)

        self.update_registers()

        self.window.mainloop()

    def update_registers(self, registers_value):
        for i, key in enumerate(registers):
            frame = tk.Frame(
                master=self.reg_frame,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i, column=0, sticky='nw')
            label = tk.Label(master=self.reg_frame, text=f"{key}")
            label.grid()
            frame.grid(row=i, column=1, sticky='nw')
            label = tk.Label(master=self.reg_frame, text=f"{registers_value[i]}")
