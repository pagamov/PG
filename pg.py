# from lib import *

class Reader_Printer:
    text = []
    def read(self, file = 'index.pg'):
        import sys
        if len(sys.argv) == 2:
            file = sys.argv[1]
        with open(file, 'r') as f:
            data = f.read()
        for line in data.splitlines():
            self.text = self.text + line.split()
        return self.text
    
    def write(self, code = '', file = 'index.c', endFree = []):
         # init all needed const for code
        HEADER = '#include <stdio.h>\n \
                  #include <string.h>\n \
                  #include <stdlib.h>\n\n'
        MAIN_START = 'int main(int argc, char *argv[]) {\n'
        MAIN_END = 'return 0;\n}'

        f = open(file, 'w')
        f.write(HEADER)
        f.write(MAIN_START)
        f.write(code + '\n')
        f.write('// free section\n')
        for item in endFree:
            f.write(f"free({item})" + ';\n')
        f.write(MAIN_END)
        f.close()
    
    def compile(self, file = 'index.c', res = 'index'):
        import os
        os.system(f'gcc {file} -o {res}')
    
    def log(self, file='Reader.log.txt'):
        f = open(file, 'w')
        for word in self.text:
            f.write(word)
            f.write(' ')
            if word in [';', ':', ';;']:
                f.write('\n')
        f.close()

class Stack:
    class States:
        DEFAULT = 1 # 
        COMMENT = 2  #
        COMMENT_END = 3 #
        DEFINE = 4  # start to check patterns and deside to state
        ASSERT = 10 # assert to a new variable
    # 
    class Types:
        STRING_TYPE = 'str_t'
        INT_TYPE = 'int_t'
        VOID_TYPE = 'void_t'
        COMMENT_TYPE = 'com_t'
        # 
        VAR_TYPE = 'var_t'
        FUNC_TYPE = 'func_t'
        IN_FUNC_TYPE = 'in_func_t'
        TOKEN_TYPE = 'token_t'
        OPERATOR_TYPE = 'oper_t'
        TYPE_TYPE = 'type_t'
    # 
    class Tokens:
        tokens = [':', ';', '(', ')', 'end']
        operators = ['+', '-', '=', '*', '/', '+=', '-=', '*=', '/=', '++', '--']
        types = ['void', 'int', 'string']
        inFuncs = ['in', 'out', 'def']

    def addVar(self, name, type, size):
        self.vars[name] = {'type': type, 'size': size}

    def addFunc(self, name, type):
        self.funcs[name] = type

    def addFree(self, varName):
        self.endFree.append(varName)

    def __init__(self):
        self.code = ''
        self.stack = []
        self.state = self.States.DEFAULT

        self.vars = dict()
        self.funcs = dict()

        self.endFree = []
    
    def collect(self):
        return self.code

    def add(self, word, verbose=False):
# add new word to stack and check it for tokens
        if word == ';;' and self.state == self.States.DEFAULT:
# find comment start
            self.state = self.States.COMMENT
            self.stack.append({'value': word, 'type': self.Types.COMMENT_TYPE})
        elif word == ';;' and self.state == self.States.COMMENT:
# find comment end
            self.colapse()
            self.state = self.States.DEFAULT
        elif word == ';' and self.state == self.States.DEFAULT:
# end of line 
            self.colapse(False)
        else:
# regular add word
            self.stack.append({'value': word, 'type': None})

    def colapse(self, verbose=False):
        if self.state == self.States.DEFAULT:
            code = ''
# mark stack with types
            self.definePattern(True)
            if verbose:
                print("\033[94mcolapse: Stack after definePattern\033[0m")
                for item in self.stack:
                    print(f"{item['value']} : {item['type']}")
                print()
# transform stack with types to code
            self.code = self.code + self.applyPattern(True)
        elif self.state == self.States.COMMENT:
            code = ''
            while True:
                p = self.stack.pop()['value']
                if p == ';;':
                    code = '\n// ' + code
                    break
                else:
                    code = p + ' ' + code
            self.code = self.code + code

    def definePattern(self, verbose=False):
        for item in self.stack:
            if item['value'] in self.vars:
                item['type'] = self.Types.VAR_TYPE
                
            elif item['value'] in self.funcs:
                item['type'] = self.Types.FUNC_TYPE

            elif item['value'] in self.Tokens.inFuncs:
                item['type'] = self.Types.IN_FUNC_TYPE

            elif item['value'] in self.Tokens.tokens:
                item['type'] = self.Types.TOKEN_TYPE

            elif item['value'] in self.Tokens.operators:
                item['type'] = self.Types.OPERATOR_TYPE

            elif item['value'].isdigit():
                item['type'] = self.Types.INT_TYPE

            elif item['value'] in self.Tokens.types:
                item['type'] = self.Types.TYPE_TYPE

        if verbose:
            print('\033[94mdefinePattern: Current stack frame:\033[0m')
            print([f"{item['value']} : {item['type']}" for item in self.stack])
            print()

    def applyPattern(self, verbose=False):
        code = ''

        if verbose:
            print("\033[94mapplyPattern: current line in applyPattern\033[0m")
            print([item['type'] for item in self.stack])
            print()

        if len(self.stack) >= 5:
            line = [item['type'] for item in self.stack[::-1][:5]][::-1]
            print(line)
            if line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, None, self.Types.OPERATOR_TYPE, self.Types.INT_TYPE]: # def type none operator int
# TODO : check if var already in self.vars param 
                code = f"\n{self.stack[-4]['value']} {self.stack[-3]['value']} {self.stack[-2]['value']} {self.stack[-1]['value']};"
                self.addVar(self.stack[-3]['value'], self.stack[-4]['value'], 4)
                for i in range(5):
                    self.stack.pop()
                return code

# forward look for def string operator
            line = [item['type'] for item in self.stack[:5]]
            if line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, None, self.Types.OPERATOR_TYPE, None]: # def type none operator string ...
# collect all word from request
                text = ' '.join([item['value'] for item in self.stack[4:]])
# add string var in self.vars
# also counting spaces via lemn of the stack to be accurated in mem managment -->       v   v   v   v   v   v   v
                code = f'\nchar * {self.stack[2]["value"]} = (char *)malloc({len(text) + len(self.stack) - 4 - 1});'
                code += f'\n{self.stack[2]["value"]} = "{text}";'
                self.addVar(self.stack[2]['value'], self.stack[1]['value'], len(text) + len(self.stack) - 4 - 1)
                self.addFree(self.stack[2]['value'])
                for i in range(len(self.stack)):
                    self.stack.pop()
                return code

        if len(self.stack) >= 4:
            line = [item['type'] for item in self.stack[::-1][:4]][::-1]
            if line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, None, self.Types.INT_TYPE]: # def string none size
                code = f"\nchar * {{self.stack[-2]['value']}} = (char *)malloc({{self.stack[-1]['value']}});"
                self.addVar(self.stack[-2]['value'], self.stack[-3]['value'], self.stack[-1]['value'])
                self.addFree(self.stack[-2]['value'])
                for i in range(4):
                    self.stack.pop()
                return code

        if len(self.stack) >= 3:
            line = [item['type'] for item in self.stack[::-1][:3]][::-1]
            if line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, None]:   # def int a ;
# TODO : add type to new var
                self.addVar(self.stack[-1]['value'], self.stack[-2]['value'], 4)
                code = f"\n{self.stack[-2]['value']} {self.stack[-1]['value']};"
                for i in range(3):
                    self.stack.pop()
                return code
# TODO : add check if var already in self.vars
            elif line == [self.Types.VAR_TYPE, self.Types.OPERATOR_TYPE, self.Types.INT_TYPE]: # var (+= -= *= /=) int ;
# TODO : check for var type
                code = f"\n{self.stack[-3]['value']} {self.stack[-2]['value']} {self.stack[-1]['value']};"
                for i in range(3):
                    self.stack.pop()
                return code
            elif line == [self.Types.VAR_TYPE, self.Types.OPERATOR_TYPE, self.Types.VAR_TYPE]: # var (+= -= *= /=) var ;
# check if they are same type
# if var int (+= -= *= /=) var int
                if self.vars[self.stack[-1]['value']]['type'] == 'int' and self.vars[self.stack[-3]['value']]['type'] == 'int':
                    code = f"\n{self.stack[-3]['value']} {self.stack[-2]['value']} {self.stack[-1]['value']};"
                for i in range(3):
                    self.stack.pop()
                return code
            elif line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, self.Types.VAR_TYPE]: # (in out) type var ;
# in int a ;
# TODO : check for var type
                if self.stack[-3]['value'] == 'in':
                    if self.stack[-2]['value'] == 'int':
                        code = f'\nscanf("%d", &{self.stack[-1]["value"]});'
                        for i in range(3):
                            self.stack.pop()
                        return code
                    elif self.stack[-2]['value'] == 'string':
                        code = f'\nscanf("%s", {self.stack[-1]["value"]});'
                        for i in range(3):
                            self.stack.pop()
                        return code
                    else:
                        raise ('\033[91mapplyPattern: out of type (in) type var\033[0m')
                elif self.stack[-3]['value'] == 'out':
                    if self.stack[-2]['value'] == 'int':
                        code = f'\nprintf("%d", {self.stack[-1]["value"]});'
                        for i in range(3):
                            self.stack.pop()
                        return code
                    elif self.stack[-2]['value'] == 'string':
                        code = f'\nprintf("%s", {self.stack[-1]["value"]});'
                        for i in range(3):
                            self.stack.pop()
                        return code
                    else:
                        raise ('\033[91mapplyPattern: out of type (out) type var\033[0m')
                    
                else:
                    raise Exception('\033[91mapplyPattern: no in func to match\033[0m')

        if len(self.stack) >= 2:
            line = [item['type'] for item in self.stack[::-1][:2]][::-1]
            if line == [self.Types.VAR_TYPE, self.Types.OPERATOR_TYPE]: # a (++ --) ;
                code = f"\n{self.stack[-2]['value']} = {self.stack[-2]['value']} {self.stack[-1]['value'][0]} 1;"
                for i in range(2):
                    self.stack.pop()
                return code
            elif line == [self.Types.OPERATOR_TYPE, self.Types.VAR_TYPE]:  # (++ --) a ;
# TODO : conflict with var += var ; 
                code = f"\n{self.stack[-1]['value']} = {self.stack[-1]['value']} {self.stack[-2]['value'][0]} 1;"
                for i in range(2):
                    self.stack.pop()
                return code
        raise Exception('\033[91mapplyPattern: cant find pattern\033[0m')
        return f'error: {self.stack}'
        
if __name__ == "__main__":
    # read code and split in apart
    r_w = Reader_Printer()
    text = r_w.read()
    r_w.log()
    print('\033[92mReading stage complete\033[0m')

    # use stack machine to preproc tokens and translate
    stack = Stack()
    for item in text:
        stack.add(item)
    code = stack.collect()
    # stack.log()
    print('\033[92mStack stage complete\033[0m')

    r_w.write(code, endFree = stack.endFree)
    print('\033[92mPut in file stage complete\033[0m')

    # and compile it
    r_w.compile()
    print('\033[92mCompile stage complete\033[0m')
