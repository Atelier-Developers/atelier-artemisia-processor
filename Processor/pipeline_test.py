from compiler import compiler
from pipeline import Pipeline
import sys

sys.setrecursionlimit(5000)  # default is 1000


def test_compiler():
    file_name = "p.asm"
    print(list(map(str, compiler(file_name))))


def test_pipeline():
    Pipeline.run("p.asm")


# test_compiler()
test_pipeline()
