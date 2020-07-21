from Components.register_file.register import Register
from gate.and_gate import And
from gate.not_gate import Not
from multiplexer.mux_mxn import Mux_mxn


class IF_ID(Register):

    def __init__(self, clock, inputs, name="IF_ID_Register"):
        # 64th bit is IF.Flush
        if_id_inputs = [And((Not(inputs[64]), inputs[i])) for i in
                        range(64)]  # Ands the Not of the flush signal with the inputs, to flush if the signal was 1
        if inputs is None:
            if_id_inputs = None
        super().__init__(clock, if_id_inputs, 65, name)  # The clock should be the AND of the clock and IF.Write
        self.instruction = None
        self.pc_address = None
        self.build()

    def build(self):
        super().build()
        out = self.outputs
        self.instruction = out[0:32]
        self.pc_address = out[32:64]

    def set_input(self, inputs):
        self.inputs = inputs
        for i in range(self.size - 1):
            self.outputs[i].set_input(And((Not(self.inputs[64]), self.inputs[i])))



    def get_instruction(self):
        return self.instruction

    def get_pc_address(self):
        return self.pc_address
