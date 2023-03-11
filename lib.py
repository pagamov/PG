
class ENV:
    # store vars funcs and there name and type
    # TODO : move these to some new place mb
    

    def __init__(self):
        pass
    
    

    def possibleTypes(self, item):
        possible_types = []
        if item in self.vars:       # var
            possible_types.append(Types.VAR_TYPE)
        elif item in self.funcs:      # func
            possible_types.append(Types.FUNC_TYPE)
        elif item in self.inFuncs:    # infunc
            possible_types.append(Types.IN_FUNC_TYPE)
        elif item in self.tokens:     # token
            possible_types.append(Types.TOKEN_TYPE)
        elif item in self.operators:  # operator
            possible_types.append(Types.OPERATOR_TYPE)
        elif item.isdigit():          # number
            possible_types.append(Types.INT_TYPE)
        elif item in self.types:      # type
            possible_types.append(Types.TYPE_TYPE)
        # TODO : what to do with this shit i dont know ???
        # if True:                    # string
        #     possible_types.append(Types.STRING_TYPE)
        if possible_types == []:
            possible_types.append(None)
            # raise Exception('possibleTypes: no types')
        return possible_types



class CompressPatterns:
    def __init__(self):
        pass

    def searchPattern(self, stack, state, env):
        if len(stack) >= 2:
            line = [item['type'][0] for item in stack[::-1][:2]][::-1]

            if line == [Types.IN_FUNC_TYPE, Types.VAR_TYPE] and stack[-1]['value'] in env.vars:
                # func var ;
                if stack[-2]['value'] == 'input':
                    pass
                elif stack[-2]['value'] == 'output':
                    pass
                else:
                    raise Exception('searchPattern: not in bould func')
                return 'in_func int_var'
        if len(stack) >= 3:
            line = [item['type'][0] for item in stack[::-1][:3]][::-1]
        if len(stack) >= 4:
            line = [item['type'][0] for item in stack[::-1][:4]][::-1]
        if len(stack) >= 5:
            line = [item['type'][0] for item in stack[::-1][:5]][::-1]
        
        raise Exception('searchPattern: pattern not found')

    def definePattern(self, stack, state, env):
        for item in stack:
            print(item)
        print('\n')
        if len(stack) >= 2:
            line = [item['type'][0] for item in stack[::-1][:2]][::-1]
            if line == [Types.IN_FUNC_TYPE, Types.VAR_TYPE] and stack[-1]['value'] in env.vars:
                code = '\n'
                if stack[-2]['value'] == 'input':
                    # input
                    code += f'scanf("%d", &{stack[-1]["value"]});'
                elif stack[-2]['value'] == 'output':
                    # output
                    code += f'printf("%d", {stack[-1]["value"]});'
                else:
                    code += ''
                    raise Exception('dont know this in build func')
                for i in range(2):
                    stack.pop()
                return code

        if len(stack) >= 3:
            line = [item['type'][0] for item in stack[::-1][:3]][::-1]
            
            if line == [Types.VAR_TYPE, Types.OPERATOR_TYPE, Types.VAR_TYPE]:
                # TODO : solve this for string vars and handle string usage
                # a + b ;
                if stack[-3]['value'] in env.vars and stack[-1]['value'] in env.vars and stack[-3]['type'] == stack[-1]['type']:
                    obj = { 'state': state, 'value': f"{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']}", 'type': [Types.INT_TYPE] }
                    for i in range(3):
                        stack.pop()
                    stack.append(obj)
                    return ''
                else:
                    raise Exception('CompressPatterns: a + b ;')
            # TODO : fix problem with '=' mb move it to dif type of operators
            elif line == [Types.VAR_TYPE, Types.OPERATOR_TYPE, Types.INT_TYPE] and stack[-2]['value'] != '=':
                # a + 3 ;
                if stack[-3]['value'] in env.vars:
                    obj = { 'state': state, 'value': f"{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']}", 'type': [Types.INT_TYPE] }
                    for i in range(3):
                        stack.pop()
                    stack.append(obj)
                    return ''
                else:
                    raise Exception('CompressPatterns: a + 3 ;')
            elif line == [Types.INT_TYPE, Types.OPERATOR_TYPE, Types.VAR_TYPE]:
                # 3 + a ;
                if stack[-1]['value'] in env.vars:
                    obj = { 'state': state, 'value': f"{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']}", 'type': [Types.INT_TYPE] }
                    for i in range(3):
                        stack.pop()
                    stack.append(obj)
                    return ''
                else:
                    raise Exception('CompressPatterns: 3 + a ;')
            elif line == [Types.INT_TYPE, Types.OPERATOR_TYPE, Types.INT_TYPE]:
                # 6 + 9 ;
                if True:
                    obj = { 'state': state, 'value': f"{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']}", 'type': [Types.INT_TYPE] }
                    for i in range(3):
                        stack.pop()
                    stack.append(obj)
                    return ''
                else:
                    raise Exception('CompressPatterns: 6 + 9 ;')
            elif line == [Types.VAR_TYPE, Types.OPERATOR_TYPE, Types.INT_TYPE]:
                # a = 4 ;
                if stack[-3]['value'] in env.vars:
                    code = f"\n{stack[-3]['value']} {stack[-2]['value']} {stack[-1]['value']};"
                    for i in range(3):
                        stack.pop()
                    return code
                else:
                    raise Exception('CompressPatterns: a = 4 ;')
            elif line == [None, Types.TOKEN_TYPE, Types.TYPE_TYPE]:
                # a : int ;
                if stack[-3]['value'] not in env.vars:
                    code = f"\n{stack[-1]['value']} {stack[-3]['value']};"
                    env.addVar(stack[-3]['value'], stack[-1]['value'])
                    for i in range(3):
                        stack.pop()
                    return code
                else:
                    raise Exception('CompressPatterns: a : int ;')

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
        
class STACK:
    code = ''
    env = ENV()
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
            # end of line so need to classify type of operation
            self.state = States.DEFINE

        # deside what to do
        if self.state == States.DEFAULT:
            # check item for any types it can be and push to stack
            possible_types = self.env.possibleTypes(item)
            self.stack.append({ 'state': self.state, 'value': item, 'type': possible_types})
        elif self.state == States.DEFINE:
            # pop operation from stack
            self.colapse(self.state)
        elif self.state == States.COMENT:
            self.stack.append({ 'state': self.state, 'value': item, 'type': [Types.COMENT_TYPE]})
        elif self.state == States.COMENT_END:
            self.colapse(self.state)
            self.state = States.DEFAULT

    def pop(self):
        return self.stack.pop()

    def log(self, file='Stack.log.txt'):
        import json
        f = open(file, 'w')
        for item in self.stack:
            f.write(json.dumps(item))
            f.write('\n')
        f.close()

    def collect(self):
        return self.code

