from compiler import compiler
from pipeline import Pipeline
import sys

from pipeline_gui import PipelineGUI

sys.setrecursionlimit(5000)  # default is 1000


def test_compiler():
    file_name = "p.asm"
    print(list(map(str, compiler(file_name))))


def test_pipeline():
    Pipeline.debug_mode("p.asm")


def test_gui():
    regs = ['1234' * 8 for _ in range(32)]
    gui = PipelineGUI()
    gui.update_registers(regs)

    gui.window.mainloop()


# test_compiler()
# test_pipeline()

test_pipeline()
# test_gui()
