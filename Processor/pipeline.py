from Components.alu.alu import ALU
from Components.control_units.control_unit import ControlUnit
from Components.control_units.alu_control_unit import ALUControlUnit
from Components.forwading_unit.forwarding_unit import ForwardingUnit
from Components.hazard_detection_unit.hazard_detection_unit import HazardDetectionUnit
from Components.pipline_register.ex_mem import EX_MEM
from Components.pipline_register.id_ex import ID_EX
from Components.pipline_register.if_id import IF_ID
from Components.pipline_register.mem_wb import MEM_WB
from Components.pipline_register.pc import PC
from Components.register_file.register_file_unit import RegisterFileUnit
from multiplexer.mux_mxn import Mux_mxn


class Pipeline:
    def __init__(self, clock):
        # Get an instruciton list maybe?

        # Components
        self.forwarding_unit: ForwardingUnit = None
        self.alu: ALU = None
        self.control_unit: ControlUnit = None
        self.alu_control_unit: ALUControlUnit = None
        self.hazard_detection_unit: HazardDetectionUnit = None
        self.register_file_unit: RegisterFileUnit = None

        # Pipeline registers
        self.pc: PC = None
        self.if_id: IF_ID = None
        self.id_ex: ID_EX = None
        self.ex_mem: EX_MEM = None
        self.mem_wb: MEM_WB = None
        self.clock = clock
        self.build()

    def build(self):

        self.ex_mem = EX_MEM(self.clock, None)
        self.mem_wb = MEM_WB(self.clock, None)
        self.id_ex = ID_EX(self.clock, None)
        self.if_id = IF_ID(self.clock, None, None)

        self.pc = PC(self.clock, None,)

        self.forwarding_unit = ForwardingUnit(
            self.ex_mem.get_rd(),
            self.mem_wb.get_rd(),
            self.ex_mem.get_wb_control()[1],
            self.mem_wb.get_wb_control()[1],
            self.id_ex.get_rs(),
            self.id_ex.get_rt(),
            "FowardingUnit"
        )

        self.hazard_detection_unit = HazardDetectionUnit(
            self.id_ex.get_mem_control()[0],
            self.id_ex.get_rt(),
            self.if_id.get_instruction()[11:16],
            self.if_id.get_instruction()[6:11],
            "HazardDetectionUnit"
        )

        self.control_unit = ControlUnit(
            self.if_id.get_instruction()[0:6],
            "ControlUnit"
        )

        self.alu_control_unit = ALUControlUnit(
            self.control_unit.output[:2],
            self.id_ex.get_funct(),
            "ALU_ControlUnit"
        )

        # todo The one in the middle should be the mux result
        mux_a = [
            Mux_mxn(
                (self.id_ex.get_read_val1()[i], self.mem_wb.ra[i], self.ex_mem.get_alu_result()[i]),
                self.forwarding_unit.outputs[0],
                2,
                f"MUX_ALU_Input_A{i}"
            ) for i in range(32)  # todo len of what?
        ]

        # todo This one too
        mux_b = [
            Mux_mxn(
                (self.id_ex.get_read_val2()[i], self.mem_wb.ar[i], self.ex_mem.get_alu_result()[i]),
                self.forwarding_unit.outputs[0],
                2,
                f"MUX_ALU_Input_B{i}"
            ) for i in range(32)  # todo len of what?
        ]

        # todo Output of mux or what???
        mux_b2 = [
            Mux_mxn(
                (mux_b[i].output, self.id_ex.get_immediate()[i]),
                None,  # TODO what is selector
                1,
                f"MUX_ALU_Input_B{i}"
            ) for i in range(32)  # todo len of what?
        ]

        self.alu = ALU(
            mux_a,
            mux_b2,
            self.alu_control_unit.output[0],
            self.alu_control_unit.output[1:],
            self.id_ex.get_immediate(),  # TODO Is SHAMT the immediate field of ID_EX????????
            "ALU"
        )

        # self.register_file_unit = RegisterFileUnit(
        #
        # )

        # self.register_file_unit = RegisterFileUnit
