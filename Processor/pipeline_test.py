from compiler import compiler


def test_compiler():
    file_name = "p.asm"

    print(list(map(len, compiler(file_name))))


test_compiler()
