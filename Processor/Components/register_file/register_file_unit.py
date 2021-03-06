from Components.register_file.register import Register
from decoder.decoder_mxn import Decoder_nxm
from gate.and_gate import And
from gate.input_gate import Input
from multiplexer.mux_mxn import Mux_mxn
from math import log


class RegisterFileUnit:

    def __init__(self, inputs, enable, clock, n, reg_width, register_clock, name="RegisterFileUnit"):
        self.inputs: tuple = inputs  # All inputs should be of type Input
        self.write_reg: Input = enable
        self.clock = clock
        self.name = name
        self.read1: list = None
        self.read2: list = None
        self.registers: list = None
        self.outputs: tuple = None
        self.dec1 = None
        self.n = n  # Number of Registers
        self.write_num_reg = None
        self.reg_width = reg_width
        self.register_clock = register_clock
        self.build()

    def __repr__(self):
        return f"{self.name} : {self.get_outputs()}"

    def build(self):
        # TODO buffer enable
        read_number1, read_number2, write_number1, write_value1 = self.inputs
        # self.write_num_reg = Register(self.register_clock, write_number1, int(log(self.n, 2)))
        self.write_num_reg = write_number1
        self.dec1 = Decoder_nxm(self.write_num_reg, int(log(self.n, 2)))
        self.registers = []
        app = self.registers.append
        for i in range(self.n):
            app(
                Register(And((self.clock, self.write_reg, self.dec1.outputs[i])), write_value1, self.reg_width))
        muxes_read1 = []
        muxes_read1_app = muxes_read1.append
        for i in range(self.reg_width):
            inputs = []
            inp_app = inputs.append
            for j in range(self.n):
                inp_app(self.registers[j].outputs[i])
            muxes_read1_app(Mux_mxn(inputs, read_number1, int(log(self.n, 2)),
                                    f"{self.name}_mux_{i}_read1"))

        muxes_read2 = []
        muxes_read2_app = muxes_read2.append
        for i in range(self.reg_width):
            inputs = []
            inp_app = inputs.append
            for j in range(self.n):
                inp_app(self.registers[j].outputs[i])
            muxes_read2_app(Mux_mxn(inputs, read_number2, int(log(self.n, 2)),
                                    f"{self.name}_mux_{i}_read1"))

        self.read1 = muxes_read1
        self.read2 = muxes_read2
        self.outputs = (self.read1, self.read2)

    def logic(self, depend=[]):
        if self in depend:
            return self.outputs
        # for i in range(self.n):
        #     self.registers[i].logic(depend + [self])
        for i in range(self.reg_width):
            self.read1[i].logic(depend + [self])
            self.read2[i].logic(depend + [self])
        return self.get_outputs()

    def get_outputs(self):
        return [self.outputs[0][i].output for i in range(self.reg_width)], [self.outputs[1][i].output for i in
                                                                            range(self.reg_width)]

    def show_content(self):
        return [''.join(map(str, self.registers[i].get_output())) for i in range(self.n)]
