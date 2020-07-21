from Components.register_file.register import Register
from gate.and_gate import And
from gate.not_gate import Not
from multiplexer.mux_mxn import Mux_mxn


class IF_ID(Register):

    def __init__(self, clock, inputs, if_flag, name="IF_ID_Register"):
        if_id_inputs = [And((Not(if_flag), inputs[i])) for i in
                        range(64)]  # Ands the Not of the flush signal with the inputs, to flush if the signal was 1
        super().__init__(clock, if_id_inputs, 64, name)  # The clock should be the AND of the clock and IF.Write
        self.if_flag = if_flag  # Should flush if 1,
        self.instruction = None
        self.pc_address = None
        self.build()

    def build(self):
        super().build()
        out = [self.outputs[i].output for i in range(len(self.outputs))]
        self.instruction = out[0:32]
        self.pc_address = out[32:64]

    def get_instruction(self):
        return self.instruction

    def get_pc_address(self):
        return self.pc_address
