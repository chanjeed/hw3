#Use Shunting-yard algorithm to change to Postfix
#Then calculate using Stack

class Stack:
    def __init__(self):
        self.items = []
        
    def isEmpty(self):
	return self.items == []
	
    def push(self, item):
	self.items.insert(0,item.copy())
        return self
	
    def pop(self):
        if not self.isEmpty():
	    return self,self.items.pop(0)
        else:
            print "Stack is empty cannot pop"
            exit(1)
	
    def peek(self):
	return self.items[0]
	
    def size(self):
	return len(self.items)
    
#Check if number of Parentheses are correct
    
def checkParenthese(line):
    check=0
    for index in range(len(line)):
        if line[index]=='(':
            check+=1
        elif line[index]==')':
            check-=1
        if check<0:
            return 'FALSE'
    if check==0:
        return 'TRUE'
    else:
        return 'FALSE'

    
# Make Number Token

def readNumber(line, index,is_minus):
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
    if is_minus=='TRUE':
        number*=-1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

# Make Operation Token

def readDivide(line,index):
    token={'type':'DIVIDE'}
    return token, index + 1


def readMultiply(line,index):
    token={'type':'MULTIPLY'}
    return token, index + 1


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readPower(line,index):
    token = {'type': 'POWER'}
    return token, index + 1

# Make Parenthese Token

def readParentheseOpen(line,index):
    token = {'type': 'ParentheseOpen'}
    return token, index + 1

def readParentheseClose(line,index):
    token = {'type': 'ParentheseClose'}
    return token, index + 1

# Make Tokens

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            minus='FALSE'
            (token, index) = readNumber(line, index,minus)
        elif line[index] == '+':
            if (not line[index-1].isdigit() and line[index-1]!=')' and line[index+1].isdigit()) or index==0 : # plus sign in front of numberex. 3*+5
                minus='FALSE'
                (token, index) = readNumber(line, index+1,minus)
            else:
                (token, index) = readPlus(line, index)
        elif line[index] == '-':
            if (not line[index-1].isdigit() and line[index-1]!=')' and line[index+1].isdigit()) or index==0 : # minus sign in front of number ex. 3*-2
                minus='TRUE'
                (token, index) = readNumber(line, index+1,minus)
            else:
                (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readParentheseOpen(line, index)
        elif line[index] == ')':
            (token, index) = readParentheseClose(line, index)
        elif line[index] == '^':
            (token, index) = readPower(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

# Precedence of operation

def OperationValue(op_type):   
    value=0
    if op_type == 'PLUS' or op_type == 'MINUS':
        value=1
    elif op_type == 'DIVIDE' or op_type == 'MULTIPLY' :
        value=2
    elif  op_type == 'POWER':
        value=3
    elif op_type=='ParentheseOpen' or  op_type=='ParentheseClose':
        return value
    else:
        print "Operation ERROR ",op_type
    return value

# makePostfix when it is a operation

def makeOperation(tokens,index,stack,output):
    ThisOpValue=OperationValue(tokens[index]['type'])
    while stack.size()!=0 :
        if ThisOpValue<=OperationValue(stack.items[0]['type']) and ThisOpValue!=3:
            (stack,pop_to_output)=stack.pop()
            output.append(pop_to_output)
        else:
            break
    stack=stack.push(tokens[index])
    return tokens,index,stack,output

# makePostfix when it is a ')'
        
def makeParentheseClose(tokens,index,stack,output):
    while stack.items[0]['type']!='ParentheseOpen' and not stack.isEmpty():
        (stack,pop_to_output)=stack.pop()
        output.append(pop_to_output)
    (stack,pop_to_output)=stack.pop()
    return tokens,index,stack,output

# it is operation or not

def is_op(type):
    if type=='PLUS' or type == 'MINUS' or type == 'DIVIDE' or type == 'MULTIPLY' or type == 'POWER':
        return 1
    else:
        return 0

# Change input into Postfix
    
def makePostfix(tokens):
    index=0
    output=[]
    stack=Stack()
    while index<len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            output.append(tokens[index])
        elif is_op(tokens[index]['type']):
            (tokens,index,stack,output)=makeOperation(tokens,index,stack,output)
        elif tokens[index]['type'] == 'ParentheseOpen':
            stack=stack.push(dict(tokens[index]))
        elif tokens[index]['type'] == 'ParentheseClose':
            (tokens,index,stack,output)=makeParentheseClose(tokens,index,stack,output)
        else:
            print 'Invalid syntax'
        index += 1
    while not stack.isEmpty():
        (stack,pop_to_output)=stack.pop()
        output.append(pop_to_output)
    return output

# Calculate each operation from Postfix

def calculate(first_num,second_num,op):
    import math
    if op=='PLUS':
        calculate=first_num+second_num
    elif op=='MINUS':
        calculate=first_num-second_num
    elif op=='DIVIDE':
        calculate=float(first_num/second_num)
    elif op=='MULTIPLY':
        calculate=first_num*second_num
    elif op=='POWER':
        calculate=math.pow(first_num,second_num)
    return calculate

# Calculate Postfix

def evaluatePostfix(tokens):
    index=0
    stack=Stack()
    while index<len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            stack=stack.push(tokens[index])
        elif is_op(tokens[index]['type']):
            (stack, second_num)=stack.pop()
            (stack, first_num)=stack.pop()
            token={'type': 'NUMBER','number': calculate(first_num['number'],second_num['number'],tokens[index]['type'])}
            stack=stack.push(token)
        else:
            print 'Invalid syntax'
        index += 1
    return stack.items[0]['number']
    

def test(line, expectedAnswer):
    tokens = tokenize(line)
    tokens =  makePostfix(tokens)
    actualAnswer = evaluatePostfix(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    print "==== Test finished! ====\n"

runTest()

while True:
    print "######Calculator######## Available Operation (+,-,*,/,^)#############"
    print 'Input> ',
    line = raw_input()
    if checkParenthese(line)=='TRUE':
        tokens = tokenize(line)
    #    print "tokenize"
    #    print tokens
        tokens = makePostfix(tokens)
    #    print "POSTFIX"
    #    print tokens
        answer = evaluatePostfix(tokens)
        print "answer = %f\n" % answer
    else :
        print "Parenthese is wrong >> Enter again"
