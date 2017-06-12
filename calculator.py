class Stack:
    def __init__(self):
        self.items = []
        
    def isEmpty(self):
        print "Check isEmpty"
	return self.items == []
	
    def push(self, item):
	self.items.insert(0,item.copy())
        return self
	
    def pop(self):
        if not self.isEmpty():
	    return self,self.items.pop(0)
        else:
            print "Stack is empty cannot pop"
	
    def peek(self):
	return self.items[0]
	
    def size(self):
	return len(self.items)

def checkParenthese(line):
    check=0
    for index in range(len(line)):
        if line[index]=='(':
            check+=1
        elif line[index]==')':
            check-=1
        if check<0:
            return 'FALSE'
    return 'TRUE'


def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def readDivide(line,index):
    token={'type':'DIVIDE'}
    return token, index + 1


def readMultiply(line,index):
    token={'type':'Multiply'}
    return token, index + 1


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readParentheseOpen(line,index):
    token = {'type': 'ParentheseOpen'}
    return token, index + 1

def readParentheseClose(line,index):
    token = {'type': 'ParentheseClose'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readParentheseOpen(line, index)
        elif line[index] == ')':
            (token, index) = readParentheseClose(line, index)            
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens




     


def empty(top):
    if top==-1:
        return 'TRUE'
    else :
        return 'FALSE'

def OperationValue(op_type):
    value=0
    if op_type == 'PLUS' or op_type == 'MINUS':
        value=1
    elif op_type == 'DIVIDE' or op_type == 'MULTIPLY' :
        value=2
    else:
        print "Operation ERROR"
    return value

def makeOperation(tokens,index,stack,output):
    ThisOpValue=OperationValue(tokens[index]['type'])
    while not stack.isEmpty():
        if ThisOpValue<OperationValue(stack.items[0]['type']):
            (stack,pop_to_output)=stack.pop()
            output.append(pop_to_output)
        else:
            break
    print "yeah"
    stack=stack.push(tokens[index])
    print "finish push"
    return tokens,index,stack,output
        
def makeParenthese(tokens,index,stack,output):
    while stack.items[0]['type']!='ParentheseOpen' and not stack.isEmpty():
        print stack.items[0]['type']
        (stack,pop_to_output)=stack.pop()
        output.append(pop_to_output)
    stack=stack.pop()
    return tokens,index,stack,output
    
def makePostfix(tokens):
    index=0
    output=[]
    stack=Stack()
    print "output is"
    print output
    while index<len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            output.append(tokens[index])
        elif tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS' or tokens[index]['type'] == 'DIVIDE' or tokens[index]['type'] == 'MULTIPLY' :
            (tokens,index,stack,output)=makeOperation(tokens,index,stack,output)
        elif tokens[index]['type'] == 'ParentheseOpen':
            print "tokens[index] ",dict(tokens[index])
            stack=stack.push(dict(tokens[index]))
        elif tokens[index]['type'] == 'ParentheseClose':
            (tokens,index,stack,output)=makeParenthese(tokens,index,stack,output)
        else:
            print 'Invalid syntax'
        index += 1
    print stack.isEmpty()
    while not stack.isEmpty():
        (stack,pop_to_output)=stack.pop()
        output.append(pop_to_output)
    return output       

#def test(line, expectedAnswer):
 #   tokens = tokenize(line)
  #  actualAnswer = evaluate(tokens)
  #  if abs(actualAnswer - expectedAnswer) < 1e-8:
   #     print "PASS! (%s = %f)" % (line, expectedAnswer)
  #  else:
   #     print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
#def runTest():
 #   print "==== Test started! ===="
  #  test("1+2", 3)
   # test("1.0+2.1-3", 0.1)
   # print "==== Test finished! ====\n"

#runTest()

while True:
    print '> ',
    line = raw_input()
    if checkParenthese(line)=='TRUE':
        tokens = tokenize(line)
        print "tokenize"
        print tokens
        tokens = makePostfix(tokens)
     #   answer = evaluatePostfix(tokens)
     #   print "answer = %f\n" % answer
        print "postfix is"
        print tokens
    else :
        print "Cannot calculate >> Enter again"
