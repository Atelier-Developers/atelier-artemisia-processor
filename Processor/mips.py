from Components.alu.alu import ALU
from Components.control_units.control_unit import ControlUnit
from Components.control_units.alu_control_unit import ALUControlUnit
from Components.forwading_unit.forwarding_unit import ForwardingUnit
from Components.hazard_detection_unit.hazard_detection_unit import HazardDetectionUnit
from Components.register_file.register_file_unit import RegisterFileUnit
from multiplexer.mux_mxn import Mux_mxn


class MIPS:
    def __init__(self):
        self.forwarding_unit: ForwardingUnit = None
        self.alu: ALU = None
        self.control_unit: ControlUnit = None
        self.alu_control_unit: ALUControlUnit = None
        self.hazard_detection_unit: HazardDetectionUnit = None
        self.register_file_unit: RegisterFileUnit = None

        self.if_id: IF_ID = None
        self.id_ex: ID_EX = None
        self.ex_mem: EX_MEM = None
        self.mem_wb: MEM_WB = None

        self.build()

    def build(self):
        self.forwarding_unit = ForwardingUnit(
            self.ex_mem.rd,
            self.mem_wb.rd,
            self.ex_mem.rw,
            self.mem_wb.rw,
            self.id_ex.rs,
            self.id_ex.rt,
            "FowardingUnit"
        )

        self.hazard_detection_unit = HazardDetectionUnit(
            self.id_ex.rm,
            self.id_ex.rt,
            self.if_id.rt,
            self.if_id.rs,
            "HazardDetectionUnit"
        )

        self.control_unit = ControlUnit(
            self.if_id.opcode,
            "ControlUnit"
        )

        self.alu_control_unit = ALUControlUnit(
            self.control_unit.output[:2],
            self.id_ex.funct,
            "ALU_ControlUnit"
        )

        mux_a = [
            Mux_mxn(
                (self.id_ex.ra[i], self.ex_mem.ar[i], self.mem_wb.ar[i]),
                self.forwarding_unit.outputs[0],
                2,
                f"MUX_ALU_Input_A{i}"
            ) for i in range(32)  # todo len of what?
        ]

        mux_b = [
            Mux_mxn(
                (self.id_ex.rb[i], self.ex_mem.ar[i], self.mem_wb.ar[i]),
                self.forwarding_unit.outputs[0],
                2,
                f"MUX_ALU_Input_B{i}"
            ) for i in range(32)  # todo len of what?
        ]
        mux_b2 = [
            Mux_mxn(
                (self.id_ex.rb[i], self.ex_mem.ar[i], self.mem_wb.ar[i]),
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
            None,  # TODO SHAMT
            "ALU"
        )

        self.register_file_unit = RegisterFileUnit(

        )

        # self.register_file_unit = RegisterFileUnit
