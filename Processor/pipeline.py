from Components.alu.alu import ALU
from Components.alu.left_shift import LeftSift
from Components.control_units.control_unit import ControlUnit
from Components.control_units.alu_control_unit import ALUControlUnit
from Components.forwading_unit.forwarding_unit import ForwardingUnit
from Components.hazard_detection_unit.hazard_detection_unit import HazardDetectionUnit
from Components.memory_hierarchy.main_memory import MainMemory
from Components.pipline_register.ex_mem import EX_MEM
from Components.pipline_register.id_ex import ID_EX
from Components.pipline_register.if_id import IF_ID
from Components.pipline_register.mem_wb import MEM_WB
from Components.pipline_register.pc import PC
from Components.register_file.register_file_unit import RegisterFileUnit
from Components.sign_extend.sign_extend_16to32 import SignExtend16To32
from adder.full_adder import FullAdder
from comparator.comparator import Comparator
from gate.and_gate import And
from gate.input_gate import Input
from gate.one_gate import One
from gate.zero_gate import Zero
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
        self.sign_extend: SignExtend16To32 = None
        self.data_cache: MainMemory = None
        self.instruction_cache: MainMemory = None

        # Pipeline registers
        self.pc: PC = None
        self.if_id: IF_ID = None
        self.id_ex: ID_EX = None
        self.ex_mem: EX_MEM = None
        self.mem_wb: MEM_WB = None
        self.clock = clock
        self.build()

    def build(self):
        # Initializing Pipeline registers

        self.ex_mem = EX_MEM(self.clock, None)
        self.mem_wb = MEM_WB(self.clock, None)
        self.id_ex = ID_EX(self.clock, None)
        self.if_id = IF_ID(self.clock, None, None)

        self.pc = PC(self.clock, None, )

        # Stage 5

        mem_wb_mux = [Mux_mxn((self.mem_wb.get_alu_result()[i], self.mem_wb.get_data_memory()[i]),
                              self.mem_wb.get_wb_control()[0], 1) for i in range(32)]

        # Stage 2

        inst = self.if_id.get_instruction()

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

        # write value = mux stage 5,
        self.register_file_unit = RegisterFileUnit((inst[6:11], inst[11:17], self.mem_wb.get_rd(), mem_wb_mux),
                                                   self.mem_wb.get_wb_control()[1], self.clock, 32, 32,
                                                   "Pipeline_Register_File")
        self.sign_extend = SignExtend16To32(inst[16:32])
        shift_sign_extend = LeftSift(self.sign_extend, [Zero(), Zero(), Zero(), One(), Zero()], 32)
        branch_adder = [FullAdder(shift_sign_extend.output[i], self.if_id.get_pc_address()[i]) for i in range(32)]
        branch_comp_input1 = [Input() for _ in range(32)]
        branch_comp_input2 = [Input() for _ in range(32)]
        branch_comparator = Comparator((self.register_file_unit.outputs[0], self.register_file_unit.outputs[1]), 32)
        branch_and = And((branch_comparator, self.control_unit.output[8]))
        zero = Zero()
        # todo careful about hazard detection output
        id_ex_mux = [Mux_mxn((self.control_unit.output[i], zero), self.hazard_detection_unit.output, 1) for i in
                     range(len(self.control_unit.output) - 2)]

        # todo WARNING input?
        id_ex_input = inst[16:21] + inst[11:16] + inst[6:11] + self.sign_extend.output + \
                      self.register_file_unit.outputs[1] + self.register_file_unit.outputs[0] + \
                      id_ex_mux[2:4] + id_ex_mux[0:2] + id_ex_mux[6:8] + id_ex_mux[4:6]

        jump_address = self.if_id.get_pc_address()[:4] + inst[6:32] + [zero for _ in range(2)]

        self.id_ex.set_input(id_ex_input)

        # Stage 3

        self.forwarding_unit = ForwardingUnit(
            self.ex_mem.get_rd(),
            self.mem_wb.get_rd(),
            self.ex_mem.get_wb_control()[1],
            self.mem_wb.get_wb_control()[1],
            self.id_ex.get_rs(),
            self.id_ex.get_rt(),
            "ForwardingUnit"
        )

        mux_forwarding_a = [
            Mux_mxn((self.id_ex.get_read_val1()[i], mem_wb_mux[i], self.ex_mem.get_alu_result()[i], zero),
                    self.forwarding_unit.get_output()[0], 2) for i in range(32)]
        mux_forwarding_b = [
            Mux_mxn((self.id_ex.get_read_val2()[i], mem_wb_mux[i], self.ex_mem.get_alu_result()[i], zero),
                    self.forwarding_unit.get_output()[1], 2) for i in range(32)]

        mux_alu_src = [
            Mux_mxn((mux_forwarding_b[i], self.id_ex.get_immediate()[i]),
                    self.id_ex.get_ex_control()[1], 1) for i in range(32)]

        self.alu_control_unit = ALUControlUnit(
            self.id_ex.get_ex_control()[2:4],
            self.id_ex.get_funct(),
            "ALU_ControlUnit"
        )

        self.alu = ALU(
            mux_forwarding_a,
            mux_alu_src,
            self.alu_control_unit.output[0],
            self.alu_control_unit.output[1:],
            self.id_ex.get_immediate()[21:26],
            "ALU"
        )

        mux_reg_dst = [
            Mux_mxn((self.id_ex.get_rd()[i], self.id_ex.get_rt()[i]),
                    self.id_ex.get_ex_control()[0], 1) for i in range(5)]

        ex_mem_inputs = mux_reg_dst + mux_alu_src + self.alu.output + self.id_ex.get_mem_control() \
                        + self.id_ex.get_wb_control()
        self.ex_mem.set_input(ex_mem_inputs)

        # Stage 4

        self.data_cache = MainMemory(self.clock, self.ex_mem.get_alu_result(), self.ex_mem.get_alu_result(),
                                     self.ex_mem.get_second_alu_src_value(), self.ex_mem.get_mem_control()[1],
                                     self.ex_mem.get_mem_control()[0], 16, "Pipeline_Data_Cache")

        mem_wb_inputs = self.ex_mem.get_rd() + self.ex_mem.get_alu_result() + self.data_cache.output + self.ex_mem.get_wb_control()
        self.mem_wb.set_input(mem_wb_inputs)

        # Stage 1

        inst_address = self.pc.get_instruction_address()
        four = [zero for _ in range(29)] + [One()] + [zero for _ in range(2)]  # 4

        # pc_adder = [FullAdder(inst_address[i], four[i]) for i in range(32)]

        # TODO set write address and value to None or Zero
        self.instruction_cache = MainMemory(self.clock, self.pc.get_instruction_address(), self.ex_mem.get_alu_result(),
                                            self.ex_mem.get_second_alu_src_value(), zero,
                                            One(), 16, "Pipeline_Instruction_Cache")
