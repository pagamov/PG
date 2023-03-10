class Color:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
class PreCode:
    # init all needed const for code
    HEADER = '#include <stdio.h>\n\n'
    MAIN_START = 'int main(int argc, char *argv[]) {\n'
    MAIN_END = 'return 0;\n}'

class States:
    DEFAULT = 1 # 
    COMENT = 2  #
    COMENT_END = 3 #
    DEFINE = 4  # start to check patterns and deside to state

    ASSERT = 10 # assert to a new variable

class Types:
    STRING_TYPE = 'str_t'
    INT_TYPE = 'int_t'
    VOID_TYPE = 'void_t'
    COMENT_TYPE = 'com_t'

    VAR_TYPE = 'var_t'
    FUNC_TYPE = 'func_t'
    IN_FUNC_TYPE = 'in_func_t'
    TOKEN_TYPE = 'token_t'
    OPERATOR_TYPE = 'oper_t'
    TYPE_TYPE = 'type_t'

class Env:
    # store vars funcs and there name and type
    # TODO : move these to some new place mb
    tokens = [':', ';', '(', ')']
    operators = ['+', '-', '=', '*', '/']
    types = ['void', 'int', 'string']
    inFuncs = ['input', 'output']

    def __init__(self):
        self.vars = dict()
        self.funcs = dict()
    
    def addVar(self, name, type):
        self.vars[name] = type

    def addFunc(self, name, type):
        self.funcs[name] = type

    def possibleTypes(self, item):
        possible_types = []
        if item in self.vars:       # var
            possible_types.append(Types.VAR_TYPE)
        if item in self.funcs:      # func
            possible_types.append(Types.FUNC_TYPE)
        if item in self.inFuncs:    # infunc
            possible_types.append(Types.IN_FUNC_TYPE)
        if item in self.tokens:     # token
            possible_types.append(Types.TOKEN_TYPE)
        if item in self.operators:  # operator
            possible_types.append(Types.OPERATOR_TYPE)
        if item.isdigit():          # number
            possible_types.append(Types.INT_TYPE)
        if item in self.types:      # type
            possible_types.append(Types.TYPE_TYPE)
        # TODO : what to do with this shit i dont know ???
        # if True:                    # string
        #     possible_types.append(Types.STRING_TYPE)
        if possible_types == []:
            possible_types.append(None)
        return possible_types

class Reader:
    text = []
    def read(self, file = 'index.c'):
        import sys
        if len(sys.argv) == 2:
            file = sys.argv[1]
        with open(file, 'r') as f:
            data = f.read()
        for line in data.splitlines():
            self.text = self.text + line.split()
    
    def collect(self):
        return self.text
    
    def log(self, file='Reader.log.txt'):
        f = open(file, 'w')
        for word in self.text:
            f.write(word)
            f.write(' ')
        f.close()

class CompressPatterns:
    def __init__(self):
        pass

    def definePattern(self, stack, state, env):
        tr = True
        while len(stack) != 0 and tr:
            for item in stack:
                print(item)
            print('\n\n')

            if len(stack) >= 2:
                line = [item['type'][0] for item in stack[::-1][:2]][::-1]
                if line == [Types.IN_FUNC_TYPE, Types.VAR_TYPE] and stack[-1]['value'] in env.vars:
                    code = '\n'
                    # input or output
                    if stack[-2]['value'] == 'input':
                        code += f'scanf("%d", &{stack[-1]["value"]});'
                    elif stack[-2]['value'] == 'output':
                        code += f'printf("%d", {stack[-1]["value"]});'
                    else:
                        code += 'null'
                        raise Exception('dont know this in build func')
                    for i in range(2):
                        stack.pop()
                    return code

            if len(stack) >= 3:
                line = [item['type'][0] for item in stack[::-1][:3]][::-1]
                print(line)
                
                if line == [Types.VAR_TYPE, Types.OPERATOR_TYPE, Types.VAR_TYPE]:
                    # TODO : solve this for string vars and handle string usage
                    # a + b ;
                    if stack[-3]['value'] in env.vars and stack[-1]['value'] in env.vars and stack[-3]['type'] == stack[-1]['type']:
                        obj = { 'state': state, 'value': f"{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']}", 'type': [Types.INT_TYPE] }
                        for i in range(3):
                            stack.pop()
                        stack.append(obj)
                    else:
                        raise Exception('CompressPatterns: assign var before init it! or diff types! Be careful :)')
                # TODO : fix problem with '=' mb move it to dif type of operators
                elif line == [Types.VAR_TYPE, Types.OPERATOR_TYPE, Types.INT_TYPE] and stack[-2]['value'] != '=':
                    # a + 3 ;
                    if stack[-3]['value'] in env.vars:
                        obj = { 'state': state, 'value': f"{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']}", 'type': [Types.INT_TYPE] }
                        for i in range(3):
                            stack.pop()
                        stack.append(obj)
                    else:
                        raise Exception('CompressPatterns: assign var before init it! or diff types! Be careful :)')
                elif line == [Types.INT_TYPE, Types.OPERATOR_TYPE, Types.VAR_TYPE]:
                    # 3 + a ;
                    if stack[-1]['value'] in env.vars:
                        obj = { 'state': state, 'value': f"{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']}", 'type': [Types.INT_TYPE] }
                        for i in range(3):
                            stack.pop()
                        stack.append(obj)
                    else:
                        raise Exception('CompressPatterns: assign var before init it! or diff types! Be careful :)')
                elif line == [Types.INT_TYPE, Types.OPERATOR_TYPE, Types.INT_TYPE]:
                    # 6 + 9 ;
                    if True:
                        obj = { 'state': state, 'value': f"{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']}", 'type': [Types.INT_TYPE] }
                        for i in range(3):
                            stack.pop()
                        stack.append(obj)
                    else:
                        raise Exception('CompressPatterns: assign var before init it! or diff types! Be careful :)')
                elif line == [Types.VAR_TYPE, Types.OPERATOR_TYPE, Types.INT_TYPE]:
                    # a = 4 ;
                    if stack[-3]['value'] in env.vars:
                        code = f"\n{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']};"
                        for i in range(3):
                            stack.pop()
                        return code
                    else:
                        pass

            if len(stack) >= 5:
                line = [item['type'][0] for item in stack[::-1][:5]][::-1]
                if line == [None, Types.TOKEN_TYPE, Types.TYPE_TYPE, Types.OPERATOR_TYPE, Types.INT_TYPE]:
                    # define new var with value
                    # a : int = 10 ;
                    code = f"\n{stack[-3]['value']} {stack[-5]['value']} {stack[-2]['value']} {stack[-1]['value']};"
                    # add new var and type
                    env.addVar(stack[-5]['value'], stack[-3]['value'])
                    for i in range(5):
                        stack.pop()
                    return code
            tr = False
        

class Stack:
    code = ''
    env = Env()
    comp_p = CompressPatterns()

    def __init__(self):
        self.stack = []
        self.state = States.DEFAULT
    
    def colapse(self, state):
        if state == States.DEFAULT:
            # default state can be at start
            pass
        elif state == States.DEFINE:
            # start search for patterns
            # while stack have items need to search for patterns
            newCode = self.comp_p.definePattern(self.stack, self.state, self.env)
            # append new code of frame to code
            self.code += newCode
            # clear stack with code
            
            self.state = States.DEFAULT
        elif state == States.COMENT_END:
            # detects coments
            res = ''
            while True:
                p = self.pop()
                assert p['state'] == States.COMENT_END or p['state'] == States.COMENT
                if p['value'] != '/#':
                    # still inside of coment
                    res = p['value'] + ' ' + res
                elif p['value'] == '/#':
                    # reached begining of coment
                    res = '// ' + res
                    break
            self.code = self.code + '\n' + res + ';'
            
    def add(self, item):
        # change state
        if item == '/#':
            # start of coment
            self.state = States.COMENT
        elif item == '#/':
            # end of coment -> colapse and add to code
            self.state = States.COMENT_END
        elif item == ';':
            # end of line so need to classyfy type of operation
            self.state = States.DEFINE

        # deside what to do
        if self.state == States.DEFAULT:
            # check item for any types it can be and push to stack
            possible_types = self.env.possibleTypes(item)
            self.stack.append({ 'state': self.state, 'value': item, 'type': possible_types})
        elif self.state == States.DEFINE:
            self.colapse(self.state)
        elif self.state == States.COMENT:
            self.stack.append({ 'state': self.state, 'value': item, 'type': [Types.COMENT_TYPE]})
        elif self.state == States.COMENT_END:
            self.colapse(self.state)
            self.state = States.DEFAULT

    def pop(self):
        return self.stack.pop()

    def log(self, file='stack.log.txt'):
        import json
        f = open(file, 'w')
        for item in self.stack:
            f.write(json.dumps(item))
            f.write('\n')
        f.close()

    def collect(self):
        return self.code
    
class Printer:
    def write(self, code = '', file = 'index.c'):
        f = open(file, 'w')
        f.write(PreCode.HEADER)
        f.write(PreCode.MAIN_START)
        f.write(code + '\n')
        f.write(PreCode.MAIN_END)
        f.close()
    
    def compile(self, file = 'index.c', res = 'index'):
        import os
        os.system(f'gcc {file} -o {res}')

if __name__ == "__main__":
    verbose = True
    reader = Reader()
    stack = Stack()
    printer = Printer()

    # read code and split in apart
    reader.read()
    text = reader.collect()
    reader.log()
    print(Color.OKGREEN + 'Reading stage complete' + Color.ENDC)

    # use stack machine to preproc tokens and translate
    for item in text:
        stack.add(item)
    stack.log()
    code = stack.collect()
    print(Color.OKGREEN + 'Stack stage complete' + Color.ENDC)
        
    # put code in file
    printer.write(code)
    print(Color.OKGREEN + 'Put in file stage complete' + Color.ENDC)

    # and compile it
    printer.compile()
    print(Color.OKGREEN + 'Compile stage complete' + Color.ENDC)
