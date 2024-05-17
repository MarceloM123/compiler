import ply.lex as lex
import sys


class Lexer(object):
    def __init__(self):
        self.lexer = None

    # Reserved words
    reserved = {
        'program': 'PROGRAM',
        'if': 'IF',
        'else': "ELSE",
        'while': 'WHILE',
        'for': 'FOR',
        'write': 'WRITE',
        'writeln': 'WRITELN',
        'int': 'INT',
        'float': 'FLOAT',
        'double': 'DOUBLE',
        'char': 'CHAR',
        'bool': 'BOOL',
        'string': 'STRING',
        'true': 'TRUE',
        'false': 'FALSE',
    }

    # List of token names
    tokens = [
                 'ID', 'SEMICOLON', 'COMA', 'ASSIGN',  # ASSIGNING
                 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',  # BRACES
                 'VAL_INT', 'VAL_FLOAT', 'VAL_DOUBLE', 'VAL_STRING', 'VAL_CHAR',  # VAR VALUE
                 'PLUS', 'MINUS', 'DIVIDE', 'TIMES', 'MOD', 'INCREMENT', 'DECREMENT',  # ARITHMETIC OPERATORS
                 'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NE', 'OR', 'AND',  # LOGICAL OPERATORS
             ] + list(reserved.values())

    # Regular expression rules for tokens
    t_OR = r'\|\|'
    t_AND = r'&&'
    t_SEMICOLON = r';'
    t_COMA = r','
    t_ASSIGN = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_VAL_STRING = r'\".*?\"'
    t_VAL_CHAR = r"'[a-zA-Z]'"
    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'-\-'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_DIVIDE = r'\/'
    t_TIMES = r'\*'
    t_MOD = r'\%'
    t_GT = r'>'
    t_LT = r'<'
    t_GTE = r'>='
    t_LTE = r'<='
    t_EQ = r'=='
    t_NE = r'!='

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    def t_VAL_FLOAT(self, t):
        r'\d+\.\d+[f|F]'
        t.value = str(t.value)
        return t

    def t_VAL_DOUBLE(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_VAL_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # If it's not in the reserved words, it's an ID, else its reserved
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    # Discard comments
    def t_COMMENT(self, _):
        r'\/\/.*'
        pass
        # No return value. Token discarded

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        sys.exit(f'LEXICAL ERROR: Illegal character "{t.value[0]}"')

    def get_tokens(self, data, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        # Give the lexer some input
        self.lexer.input(data)

        all_tokens = []
        # Tokenize
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No more input
            all_tokens.append((tok.type, tok.value))
        return all_tokens
