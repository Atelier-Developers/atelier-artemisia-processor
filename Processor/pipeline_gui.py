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
        topframe = tk.Frame(master=self.window, width=500, height=250)
        topframe.pack(fill=tk.BOTH, expand=True)

        self.window.title("Artemisia x32 Atelier Co.")

        self.reg_frame = tk.Frame(master=topframe, height=200, width=400)
        self.reg_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.history_frame = tk.Frame(master=topframe, width=100)
        self.history_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.option_frame = tk.Frame(master=self.window, height=50, bg='blue', pady=10)
        self.option_frame.pack(fill=tk.BOTH, expand=True)

        self.mem_ad = tk.Entry(master=self.option_frame, width=25)
        self.mem_ad.grid(row=0, column=0, padx=(5, 0))

        self.mem_lbl = tk.Label(master=self.option_frame, text='', bg='blue', fg='white')
        self.mem_lbl.grid(row=1, column=0, padx=(5, 0))

        self.reg_labels = {}

    def update_registers(self, registers_value):
        if self.reg_labels.get("$zero"):
            for i, key in enumerate(registers):
                self.reg_labels[key]['text'] = registers_value[i]
        else:
            tmp = 0
            frame = tk.Frame(
                master=self.reg_frame,
                relief=tk.RAISED,
                borderwidth=1,
            )
            frame.grid(row=0, column=1, sticky='nw', columnspan=3, padx=(170, 0))  # 17/16=1
            label = tk.Label(master=frame, text=f"REGISTERS", font=("Helvetica", 30), justify=tk.CENTER)
            label.pack(fill=tk.X, expand=True)
            for i, key in enumerate(registers):
                if i % 16 == 0 and i != 0:
                    tmp = 1
                frame = tk.Frame(
                    master=self.reg_frame,
                    relief=tk.RAISED,
                    borderwidth=1
                )

                # TODO MAYBE CHANGE THE PADDING AND STUFF TO REMOVE THE EXTRA SPACE IN THE WINDOW (TO THE RIGHT)
                frame.grid(row=(i % 16) + 1, column=2 * tmp, sticky='nw')  # 17/16=1
                label = tk.Label(master=frame, text=f"{key}")
                label.pack()
                self.reg_labels[f"{key}_key"] = label
                frame = tk.Frame(
                    master=self.reg_frame,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=(i % 16) + 1, column=2 * tmp + 1, sticky='nw')
                label = tk.Label(master=frame, text=f"{registers_value[i]}")
                label.pack()
                self.reg_labels[f"{key}_value"] = label

    def make_listener(self, pipeline):
        pulse_btn = tk.Button(master=self.option_frame, text="PULSE", command=pipeline.pulse)
        pulse_btn.grid(row=0, column=10, padx=(110, 0))

        self.btn_convert = tk.Button(master=self.option_frame, text='Show memory value at address',
                                     font=("Helvetica", 10), padx=0, pady=0,
                                     command=pipeline.show_data_memory_content_gui)
        self.btn_convert.grid(row=0, column=3, padx=5)
