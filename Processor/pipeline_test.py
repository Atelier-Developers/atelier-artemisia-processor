from compiler import compiler


def test_compiler():
    file_name = "p.asm"
    print(list(map(str, compiler(file_name))))


test_compiler()
