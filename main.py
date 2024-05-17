from Lexer import Lexer
from Parser import Parser
from ICG import ICG
from VirtualMachine import VirtualMachine
import os


def main():
    # Get code to interpret
    dir_path = os.getcwd()
    contents = os.listdir(dir_path + '/codes')

    # Choose which code
    for i, filename in enumerate(contents):
        print(f'{i}: {filename}')
    selected = input('Escribe el código de prueba a utilizar: ')
    with open(dir_path + '/codes/' + contents[int(selected)], 'r') as file:
        code = file.read()

    lexer = Lexer()
    tokens = lexer.get_tokens(code)

    print(tokens)

    # parser = Parser()
    # ast = parser.parse(tokens)
    #
    # icg = ICG()
    # quadruples, declarations = icg.generate(ast)
    #
    # vm = VirtualMachine(quadruples, declarations)
    # vm.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
