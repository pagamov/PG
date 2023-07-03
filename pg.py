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
    
    def write(self, code = '', file = 'index.c', funcsBool = [], endFree = []):
        # init all needed const for code
        # endFree - vars malloc allocated need to be deleted
        HEADER = '#include <stdio.h> \
                  \n#include <string.h> \
                  \n#include <stdlib.h>\n\n'
        MAIN_START = 'int main(int argc, char *argv[]) {\n'
        MAIN_END = 'return 0;\n}'

        f = open(file, 'w')
        f.write(HEADER)
        for item in funcsBool:
            f.write("\n{}".format(item))
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

    class Types:
        STRING_TYPE = 'str_t'
        INT_TYPE = 'int_t'
        VOID_TYPE = 'void_t'
        COMMENT_TYPE = 'com_t'
        BOOL_TYPE = 'bool_t'
        # 
        VAR_TYPE = 'var_t'
        FUNC_TYPE = 'func_t'
        IN_FUNC_TYPE = 'in_func_t'
        TOKEN_TYPE = 'token_t'
        OPERATOR_TYPE = 'oper_t'
        TYPE_TYPE = 'type_t'
        BOOL_OPERATOR_TYPE = 'bool_oper_t'

    class Tokens:
        tokens = [':', ';', '(', ')', 'end']
        operators = ['+', '-', '=', '*', '/', '+=', '-=', '*=', '/=', '++', '--']
        bool_operators = ['==', '>', '<', '>=', '<=']
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

        self.funcsBool = [] # store text of all bool funcs
        self.endFree = [] # store names of all malloc vars via string
    
    def collect(self):
        return self.code

    def add(self, word, verbose = False):
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
            self.colapse(verbose)
        else:
            # regular add word
            self.stack.append({'value': word, 'type': None})

    def colapse(self, verbose=False):
        if self.state == self.States.DEFAULT:
            code = ''
            # mark stack with types
            self.definePattern(verbose)
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

            elif item['value'] in self.Tokens.bool_operators:
                item['type'] = self.Types.BOOL_OPERATOR_TYPE

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
            if line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, None, self.Types.OPERATOR_TYPE, self.Types.INT_TYPE]: # def type none operator int
                typ = self.stack[-4]['value']      # int
                variable = self.stack[-3]['value'] # var
                operator = self.stack[-2]['value'] # =
                value = self.stack[-1]['value']    # value
                code = "\n{} {} {} {};".format(typ, variable, operator, value)
                self.addVar(self.stack[-3]['value'], self.stack[-4]['value'], 4)
                for i in range(5):
                    self.stack.pop()
                return code

            # forward look for def string operator
            line = [item['type'] for item in self.stack[:5]]
            if line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, None, self.Types.OPERATOR_TYPE, None]: # def type none operator string ...
                # collect all word from request
                text = ' '.join([item['value'] for item in self.stack[4:]])
                # TODO : check if this working properly this was written at night
                variable = self.stack[2]["value"]
                size = len(text) + len(self.stack) - 4 - 1
                typ = self.stack[1]['value']
                # also counting spaces via len of the stack to be accurated in mem managment
                code = '\nchar * {} = (char *)malloc({});'.format(variable, size)
                code += '\n{} = "{}";'.format(variable, text)
                # add string var in self.vars
                self.addVar(variable, typ, size)
                # add variable to free list
                self.addFree(variable)
                # clear self.stack
                for i in range(len(self.stack)):
                    self.stack.pop()
                return code

        if len(self.stack) >= 4:
            line = [item['type'] for item in self.stack[::-1][:4]][::-1]
            if line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, None, self.Types.INT_TYPE]: # def string none size
                variable = self.stack[-2]['value']
                size = self.stack[-1]['value']
                typ = self.stack[-3]['value']
                code = "\nchar * {} = (char *)malloc({});".format(variable, size)
                self.addVar(variable, typ, size)
                self.addFree(variable)
                for i in range(4):
                    self.stack.pop()
                return code

        if len(self.stack) >= 3:
            line = [item['type'] for item in self.stack[::-1][:3]][::-1]
            if line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, None]:   # def int a ;
                # TODO : add type to new var
                typ = self.stack[-2]['value']
                variable = self.stack[-1]['value']
                size = 4
                code = "\n{} {};".format(typ, variable)
                self.addVar(variable, typ, size)
                for i in range(3):
                    self.stack.pop()
                return code
                # TODO : add check if var already in self.vars
            elif line == [self.Types.VAR_TYPE, self.Types.OPERATOR_TYPE, self.Types.INT_TYPE]: # var (+= -= *= /=) int ;
                # TODO : check for var type
                variable = self.stack[-3]['value']
                operator = self.stack[-2]['value']
                value = self.stack[-1]['value']
                code = "\n{} {} {};".format(variable, operator, value)
                for i in range(3):
                    self.stack.pop()
                return code
            elif line == [self.Types.VAR_TYPE, self.Types.OPERATOR_TYPE, self.Types.VAR_TYPE]: # var (+= -= *= /=) var ;
                # check if they are same type
                variable1 = self.stack[-1]['value']
                variable2 = self.stack[-3]['value']
                variable1Type = self.vars[variable1]['type']
                variable2Type = self.vars[variable2]['type']
                operator = self.stack[-2]['value']
                # if var int (+= -= *= /=) var int
                if variable1Type == 'int' and variable2Type == 'int':
                    code = "\n{} {} {};".format(variable2, operator, variable1)
                else:
                    raise Exception('\033[91mapplyPattern: var += var not int\033[0m')
                for i in range(3):
                    self.stack.pop()
                return code
            elif line == [self.Types.IN_FUNC_TYPE, self.Types.TYPE_TYPE, self.Types.VAR_TYPE]: # (in out) type var ;
                # in int a ;
                # TODO : check for var type
                func = self.stack[-3]['value']
                typ = self.stack[-2]['value']
                variable = self.stack[-1]["value"]
                code = ''
                if func == 'in':
                    if typ == 'int':
                        code += '\nscanf("%d", &{});'.format(variable)
                    elif typ == 'string':
                        code += '\nscanf("%s", {});'.format(variable)
                    else:
                        raise ('\033[91mapplyPattern: out of type (in) type var\033[0m')
                elif func == 'out':
                    if typ == 'int':
                        code += '\nprintf("%d", {});'.format(variable)
                    elif typ == 'string':
                        code += '\nprintf("%s", {});'.format(variable)
                    else:
                        raise ('\033[91mapplyPattern: out of type (out) type var\033[0m')
                else:
                    raise Exception('\033[91mapplyPattern: no in func to match\033[0m')
                for i in range(3):
                    self.stack.pop()
                return code
            elif line == [self.Types.VAR_TYPE, self.Types.BOOL_OPERATOR_TYPE, self.Types.INT_TYPE]: # var (== > < >= <=) int
                variable = self.stack[-3]['value']
                operator = self.stack[-2]['value']
                value = self.stack[-1]['value']
                # add check for int type
                variableType = self.vars[variable]['type']
                if variableType == 'int':
                    code = "({} {} {})".format(variable, operator, value)
                    for i in range(3):
                        self.stack.pop()
                    self.stack.append({'value': code, 'type': self.Types.BOOL_TYPE})
                    return ''
                else:
                    raise Exception('\033[91mapplyPattern: var (== > < >= <=) int Not int\033[0m')
            elif line == [self.Types.VAR_TYPE, self.Types.BOOL_OPERATOR_TYPE, self.Types.VAR_TYPE]: # var (== > < >= <=) int
                variable1 = self.stack[-3]['value']
                operator = self.stack[-2]['value']
                variable2 = self.stack[-1]['value']
                # add check for int type
                variable1Type = self.vars[variable1]['type']
                variable2Type = self.vars[variable2]['type']
                if variable1Type == 'int' and variable2Type == 'int':
                    code = "({} {} {})".format(variable1, operator, variable2)
                    for i in range(3):
                        self.stack.pop()
                    self.stack.append({'value': code, 'type': self.Types.BOOL_TYPE})
                    return ''
                else:
                    raise Exception('\033[91mapplyPattern: var (== > < >= <=) var one of them not int\033[0m')

        if len(self.stack) >= 2:
            line = [item['type'] for item in self.stack[::-1][:2]][::-1]
            if line == [self.Types.VAR_TYPE, self.Types.OPERATOR_TYPE]: # a (++ --) ;
                variable = self.stack[-2]['value']
                operator = self.stack[-1]['value'][0]
                code = "\n{} = {} {} 1;".format(variable, variable, operator)
                for i in range(2):
                    self.stack.pop()
                return code
            elif line == [self.Types.OPERATOR_TYPE, self.Types.VAR_TYPE]:  # (++ --) a ;
                # TODO : conflict with var += var ; 
                variable = self.stack[-1]['value']
                operator = self.stack[-2]['value'][0]
                code = "\n{} = {} {} 1;".format(variable, variable, operator)
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

    r_w.write(code, funcsBool = stack.funcsBool, endFree = stack.endFree)
    print('\033[92mPut in file stage complete\033[0m')

    # and compile it
    r_w.compile()
    print('\033[92mCompile stage complete\033[0m')
