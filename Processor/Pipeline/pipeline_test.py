from Compiler.compiler import compiler
from Pipeline.pipeline import Pipeline
import sys

from GUI.pipeline_gui import PipelineGUI

sys.setrecursionlimit(5000)  # default is 1000


def test_compiler():
    file_name = "p.art"
    print(list(map(str, compiler(file_name))))


def test_pipeline():
    print("WELCOME TO ARTEMISIA X32")
    print("Atelier Co.\n")
    print("Enter your file name: ")
    file_name = input()
    print()
    Pipeline.run(file_name)


def test_gui():
    regs = ['1234' * 8 for _ in range(32)]
    gui = PipelineGUI()
    gui.update_registers(regs)

    gui.window.mainloop()


# test_compiler()
# test_pipeline()
test_pipeline()
# test_gui()
