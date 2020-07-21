from compiler import compiler
from pipeline import Pipeline


def test_compiler():
    file_name = "p.asm"
    print(list(map(str, compiler(file_name))))



def test_pipeline():
    Pipeline.run("p.asm")


# test_compiler()
test_pipeline()