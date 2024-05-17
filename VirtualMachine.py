import sys


# MISSING:
# AGREGAR EL TYPE DE VARIABLE A LA MEMORIA PARA FACILITAR BUSQUEDA
# REESCRIBIR REVISION SEMANTICA A BASE DE ESO
# CHECK FOR POSSIBLE ERRORS
# TEMP VARS NEED TO HAVE THE SAME TYPE AS ITS MAIN VAR

class VirtualMachine:
    def __init__(self, quadruples, declarations):
        self.quadruples = quadruples
        self.declarations = declarations
        self.memory = {}
        self.output = []
        # Run var declarations
        self.declare_vars()

    def declare_vars(self):
        for var in self.declarations:
            var_type, var_name, var_val = var
            match var_type:
                case 'int':
                    self.memory[var_name] = 0 if var_val is None else var_val
                case 'float':
                    self.memory[var_name] = 0.0 if var_val is None else var_val
                case 'string':
                    self.memory[var_name] = "" if var_val is None else var_val
                case 'bool':
                    self.memory[var_name] = False if var_val is None else var_val
                case 'char':
                    self.memory[var_name] = '' if var_val is None else var_val
                case 'double':
                    self.memory[var_name] = 0.0 if var_val is None else var_val

    def logical_op(self, op, arg1, arg2, res):
        # Only valid types are ints, floats, bools and chars (check startswith and endswith for "'")
        if ((
                isinstance(arg1, (int, float, bool)) or
                (isinstance(arg1, str) and arg1.startswith("'") and arg1.endswith("'"))
        ) and (
                isinstance(arg2, (int, float, bool)) or
                (isinstance(arg2, str) and arg1.startswith("'") and arg1.endswith("'"))
        )):
            # Check if the value to assign has been declared or is a temp variable
            pass
        else:
            sys.exit(
                f'SEMANTIC ERROR: Incompatible types for operation: {type(arg1).__name__} and \
                {type(arg2).__name__}.'
            )

        # Check if arg1 and arg2 are of the same type
        # if type(arg1) != type(arg2):
        #     # Only valid types are ints, floats, and chars
        #     if not isinstance(arg1, (int, float, str)) and isinstance(arg2, (int, float, str)):
        #         sys.exit(
        #             f'SEMANTIC ERROR: Incompatible types for operation: {type(arg1).__name__} and \
        #             {type(arg2).__name__}.'
        #         )

        # Check if the value to assign has been declared or is a temp variable
        # if res.startswith('T') or self.memory.get(res) is not None:
        #     # Check if one of the values are chars, if either is, get its ASCII value
        #     if isinstance(arg1, str) or isinstance(arg2, str):
        #         if isinstance(arg1, str) and len(arg1) == 1:
        #             arg1 = ord(arg1)
        #         if isinstance(arg2, str) and len(arg2) == 1:
        #             arg1 = ord(arg2)
        #     # Variable exists
        #     match op:
        #         case '<':
        #             self.memory[res] = arg1 < arg2
        #         case '>':
        #             self.memory[res] = arg1 > arg2
        #         case '<=':
        #             self.memory[res] = arg1 <= arg2
        #         case '>=':
        #             self.memory[res] = arg1 >= arg2
        # else:
        #     sys.exit(f'SEMANTIC ERROR: variable {res} was not declared.')

    def arithmetic_op(self, op, arg1, arg2, res):
        # Check if arg1 and arg2 are of the same type
        if type(arg1) != type(arg2):
            if not (type(arg1).__name__ in {'int', 'float', 'bool'} and
                    type(arg2).__name__ in {'int', 'float', 'bool'}):
                sys.exit(
                    f'SEMANTIC ERROR: Incompatible types for operation: {type(arg1).__name__} and \
                    {type(arg2).__name__}.')

        # First check if the value to assign has been declared or is a temp variable
        if res.startswith('T') or self.memory.get(res) is not None:
            # Only values that are able to be operated are ints, floats and strings
            if isinstance(arg1, (int, float, str)) and isinstance(arg2, (int, float, str)):
                if op != '+' and isinstance(arg1, str) and isinstance(arg2, str):
                    sys.exit(f'SEMANTIC ERROR: Operator {op} cannot be applied to string')
                match op:
                    case '+':
                        # String concatenation
                        if isinstance(arg1, str) and isinstance(arg2, str):
                            self.memory[res] = arg1.strip('"') + arg2.strip('"')
                        else:
                            self.memory[res] = arg1 + arg2
                    case '-':
                        self.memory[res] = arg1 - arg2
                    case '*':
                        self.memory[res] = arg1 * arg2
                    case '/':
                        if arg2 != 0:
                            # If values are int, result is a whole number, else it's a number with decimals
                            if isinstance(arg1, float) or isinstance(arg2, float):
                                self.memory[res] = float(arg1 / arg2)
                            else:
                                self.memory[res] = int(arg1 / arg2)
                        else:
                            sys.exit(f'ERROR: can\'t divide by zero')
            else:
                sys.exit(f'SEMANTIC ERROR: Operator {op} cannot be applied to operands of type {type(arg1).__name__}\
                and {type(arg2).__name__}.')
        else:
            sys.exit(f'SEMANTIC ERROR: variable {res} was not declared.')

    def equality_op(self, op, arg1, arg2, res):
        if type(arg1) != type(arg2) and not (isinstance(arg1, (int, float)) and isinstance(arg2, (int, float))):
            sys.exit(
                f'SEMANTIC ERROR: Type mismatch in comparison between {type(arg1).__name__} and {type(arg2).__name__}.'
            )
        if res.startswith('T') or self.memory.get(res) is not None:
            if op == '==':
                self.memory[res] = arg1 == arg2
            elif op == '!=':
                self.memory[res] = arg1 != arg2
        else:
            sys.exit(f'SEMANTIC ERROR: Result variable {res} not declared.')

    def print_to_console(self, op, arg1):
        eop = 'new-line' if op == 'writeln' else 'no-new-line'
        if isinstance(arg1, str) and arg1.startswith('"') and arg1.endswith('"'):  # String
            self.output.append((arg1.strip('"'), eop))  # Handle direct string outputs
        elif isinstance(arg1, str) and arg1.startswith("'") and arg1.endswith("'"):  # Char
            self.output.append((arg1.strip('"'), eop))  # Handle direct string outputs
        else:
            self.output.append((str(arg1), 'new-line'))  # Handle variable outputs

    def get_declared_type(self, var_name):
        for var_type, name in self.declarations:
            if name == var_name:
                return var_type
        sys.exit(f'SEMANTIC ERROR: Variable {var_name} not declared.')

    def assign_value(self, res, value):
        # Since we are assigning to declared variables, we don't need to check for temp vars
        if res in self.memory:
            # Get the original declaration of the variable from the declarations list
            declared_type = self.get_declared_type(res)
            value_type = type(value).__name__  # We only want the builtin type name

            # Handle type compatibility and conversion
            if declared_type == value_type:
                self.memory[res] = value
            elif (declared_type == 'char' and isinstance(self.memory[res], str)) and value_type == 'str':
                if len(value) == 1:
                    self.memory[res] = value
                else:
                    sys.exit(f'SEMANTIC ERROR: Char variable {res} can only hold a single character.')
            elif declared_type == 'int' and value_type in {'int', 'bool'}:
                self.memory[res] = int(value)
            elif declared_type == 'float' and value_type in {'int', 'bool'}:
                self.memory[res] = float(value)
            elif declared_type == 'double' and value_type in {'int', 'float'}:
                self.memory[res] = float(value)
            else:
                sys.exit(
                    f'SEMANTIC ERROR: Incompatible types for assignment: {declared_type.__name__} and \
                    {value_type.__name__}.'
                )
        else:
            sys.exit(f'SEMANTIC ERROR: Result variable {res} not declared.')

    def build(self):
        pc = 0
        while pc < len(self.quadruples):
            op, arg1, arg2, res = self.quadruples[pc]
            # Fetch values if identifiers are variables
            arg1 = self.memory[arg1] if arg1 in self.memory else arg1
            arg2 = self.memory[arg2] if arg2 in self.memory else arg2

            # ASSIGN
            if op == '=':
                # We make sure the variable has already been declared
                if self.memory.get(res) is not None:
                    self.assign_value(res, arg1)
                else:
                    sys.exit(f'SEMANTIC ERROR: variable {res} was not declared.')

            # LESS THAN, GREATER THAN, LESS THAN OR EQUALS, GREATER THAN OR EQUALS
            elif op in {'<', '>', '<=', '>='}:
                self.logical_op(op, arg1, arg2, res)

            # EQUALS, NOT EQUALS
            elif op == {'==', '!='}:
                self.equality_op(op, arg1, arg2, res)

            # PLUS, MINUS, TIMES, DIVIDE
            elif op in {'+', '-', '*', '/'}:
                self.arithmetic_op(op, arg1, arg2, res)

            # PRINT
            elif op in {'writeln', 'write'}:
                self.print_to_console(op, arg1)

            # GOTO F
            elif op == 'gotoF':
                if not arg1:
                    pc = res
                    continue

            # GOTO V
            elif op == 'gotoV':
                if arg1:
                    pc = res
                    continue

            # GOTO
            elif op == 'goto':
                pc = res
                continue

            pc += 1  # Increment Program Counter

    def run(self):
        self.build()
        # Output the results
        if self.output:
            print("*** Output ***")
            for line in self.output:
                if line[1] == 'new-line':
                    print(line[0])
                else:
                    print(line[0], end='')
        else:
            print("No output generated.")
        print(self.memory)
        self.memory.clear()
        self.output.clear()


# TEST 1 - DOUBLE FOR
# quadruples = [
#     ['=', 0, None, 'i'],  # 0
#     ['<', 'i', 20, 'T1'],  # 1
#     ['gotoF', 'T1', None, 16],  # 2
#     ['gotoV', 'T1', None, 6],  # 3
#     ['+', 'i', 1, 'i'],  # 4
#     ['goto', None, None, 1],  # 5
#     ['=', 0, None, 'z'],  # 6
#     ['<', 'z', 20, 'T2'],  # 7
#     ['gotoF', 'T2', None, 15],  # 8
#     ['gotoV', 'T2', None, 12],  # 9
#     ['+', 'z', 1, 'z'],  # 10
#     ['goto', None, None, 7],  # 11
#     ['+', 'a', 'i', 'T3'],  # 12
#     ['+', 'T3', 'z', 'T4'],  # 13
#     ['goto', None, None, 10],  # 14
#     ['goto', None, None, 4],  # 15
# ]
#
# declarations = [
#     ('int', 'i'),
#     ('int', 'z'),
#     ('int', 'a'),
# ]

# TEST 2 - FOR
quadruples = [
    ['writeln', '"texto dump"', None, None],  # 0
    ['=', 5, None, 'f'],  # 1
    ['=', 0, None, 'x'],  # 2
    ['<', 'x', 'f', 'T1'],  # 3
    ['gotoF', 'T1', None, 11],  # 4
    ['gotoV', 'T1', None, 8],  # 5
    ['+', 'x', 1, 'x'],  # 6
    ['goto', None, None, 3],  # 7
    ['+', 'x', 'f', 'T2'],  # 8
    ['=', 'T2', None, 'n'],  # 9
    ['goto', None, None, 6],  # 10
    ['+', 0, '"meh"', 'T3'],  # 11
    ['writeln', 'T3', None, None]  # 12
]

declarations = [
    ('int', 'i', None),
    ('int', 'n', None),
    ('int', 'f', None),
    ('int', 'x', None)
]

# TEST 3 - IF ELSE
# quadruples = [
#     ['=', 5, None, 'A'],  # 0
#     ['=', 15, None, 'B'],  # 1
#     ['=', 53, None, 'C'],  # 2
#     ['=', 24, None, 'D'],  # 3
#     ['=', 3, None, 'E'],  # 4
#     ['>', 'A', 'B', 'T1'],  # 5
#     ['gotoF', 'T1', None, 9],  # 6
#     ['writeln', 'B', None, None],  # 7
#     ['goto', None, None, 18],  # 8
#     ['>', 'A', 'C', 'T2'],  # 9
#     ['gotoF', 'T2', None, 13],  # 10
#     ['writeln', 'C', None, None],  # 11
#     ['goto', None, None, 18],  # 12
#     ['>', 'A', 'D', 'T3'],  # 13
#     ['gotoF', 'T3', None, 17],  # 14
#     ['writeln', 'D', None, None],  # 15
#     ['goto', None, None, 18],  # 16
#     ['writeln', 'E', None, None]  # 17
# ]
#
# declarations = [
#     ('int', 'A'),
#     ('int', 'B'),
#     ('int', 'C'),
#     ('int', 'D'),
#     ('int', 'E'),
# ]

# TEST 4 - WHILE'S
# quadruples = [
#     ['=', 10, None, 'x'],  # 0 - Assign x = 10
#     ['=', 5, None, 'y'],  # 1 - Assign y = 5
#     ['=', 20, None, 'z'],  # 2 - Assign z = 20
#     ['<', 'x', 'y', 'T1'],  # 3 - Compare x < y
#     ['gotoF', 'T1', None, 11],  # 4 - Go to line 11 if T1 is false
#     ['<', 'y', 'z', 'T2'],  # 5 - Compare y < z
#     ['gotoF', 'T2', None, 10],  # 6 - Go to line 10 if T2 is false
#     ['+', 'y', 'x', 'T3'],  # 7 - y + x
#     ['=', 'T3', None, 'y'],  # 8 - Assign result of y+x to y
#     ['goto', None, None, 5],  # 9 - Go back to line 5
#     ['goto', None, None, 3],  # 10 - Go back to line 3 (this is never reached due to line 9)
# ]
#
# declarations = [
#     ('int', 'x'),
#     ('int', 'y'),
#     ('int', 'z'),
# ]

# TEST 5 - ALL COMBINED
# quadruples = [
#     ['=', 0, None, 'x'],  # 0 - Initialize x
#     ['=', 20, None, 'y'],  # 1 - Initialize y
#     ['=', 200, None, 'z'],  # 2 - Initialize z
#     ['writeln', '"Starting for loop"', None, None],  # 3 - Indicate for loop start
#     []
# ]
#
# declarations = [
#     ('int', 'x'),
#     ('int', 'y'),
#     ('int', 'z'),
#     ('int', 'i')  # for loop counter
# ]

vm = VirtualMachine(quadruples, declarations)
try:
    vm.run()
except Exception as e:
    print(f'Error en VM: {e}')
