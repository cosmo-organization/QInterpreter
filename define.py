class Token:
    def __init__(self, value, type, line, col, file="<stdin>"):
        self.value = value
        self.type = type
        self.line = line
        self.col = col
        self.file = file


##########################
####### Expression #######
##########################
class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op


class NumberExp:
    def __init__(self, tok):
        self.tok = tok


class UnaryExp:
    def __init__(self, fact):
        self.fact = fact


class VarExp:
    def __init__(self, tok):
        self.tok = tok


class VarAssignExp:
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp


class MultiVarAssignExp:
    def __init__(self, listexp):
        self.listexp = listexp


class CompoundStatement:
    def __init__(self, statements):
        self.statements = statements
        self.counter = 0

    def havenext(self):
        return True if self.counter < len(self.statements) else False

    def next(self):
        self.counter += 1
        return self.statements[self.counter - 1]

    def setjump(self, counter):
        self.counter = counter

    def getjump(self):
        return self.counter


class LoopStatement:
    def __init__(self, var=None, condition=None, times=None, body=None):
        self.condition = condition
        self.var = var
        self.times = times
        self.body = body

class Statements:
    def __init__(self, statements):
        self.statements = statements
        self.counter = 0

    def havenext(self):
        return True if self.counter < len(self.statements) else False

    def next(self):
        self.counter += 1
        return self.statements[self.counter - 1]

    def setjump(self, counter):
        self.counter = counter

    def getjump(self):
        return self.counter


class IfStatement:
    def __init__(self, condition, ifbody, elsebody, elseifbodies):
        self.ifbody = ifbody
        self.elsebody = elsebody
        self.elseifbodies = elseifbodies
        self.condition = condition


class ReturnStatement:
    def __init__(self, exp):
        self.exp = exp


class PrintStatement:
    def __init__(self, args):
        self.args = args


class LineExp:
    def __init__(self, exp):
        self.exp = exp


class SpaceExp:
    def __init__(self, exp):
        self.exp = exp


class IdExp:
    def __init__(self, exp):
        self.exp = exp


class JumpExp:
    def __init__(self, idexp, timeexp=None, conditionexp=None):
        self.idexp = idexp
        self.timeexp = timeexp
        self.conditionexp = conditionexp
        self.counter = 0
        self.out = -1


class TupleExp:
    def __init__(self, args):
        self.args = args


class ListExp:
    def __init__(self, data):
        self.data = data


class StringExp:
    def __init__(self, tok):
        self.tok = tok


class GlobalExp:
    def __init__(self, exp):
        self.exp = exp
class PyFuncExp:
    def __init__(self,name,args):
        self.name=name
        self.args=args

class FuncExp:
    def __init__(self,name,args,body):
        self.name=name
        self.args=args
        self.body=body
class FuncCallExp:
    def __init__(self,name,args,typecall='FID'):
        self.name=name
        self.args=args
        self.typecall=typecall
class SelfReplaceExp:
    def __init__(self,var,toreplace,withreplace):
        self.var=var
        self.toreplace=toreplace
        self.withreplace=withreplace

class AssignReplaceExp:
    def __init__(self,var,toreplace,withreplace):
        self.var = var
        self.toreplace = toreplace
        self.withreplace = withreplace
#########################
##### Values ############
#########################
class Value:
    def __init__(self, value):
        self.value = value

    def __truediv__(self, other):
        return Value(self.value / other.value)

    def __add__(self, other):
        return Value(self.value + other.value)

    def __sub__(self, other):
        return Value(self.value - other.value)

    def __mul__(self, other):
        return Value(self.value * other.value)

    def __lt__(self, other):
        return Value(self.value < other.value)

    def __gt__(self, other):
        return Value(self.value > other.value)

    def __le__(self, other):
        return Value(self.value <= other.value)

    def __ge__(self, other):
        return Value(self.value >= other.value)

    def __eq__(self, other):
        return Value(self.value == other.value)

    def __ne__(self, other):
        return Value(self.value != other.value)

    def __or__(self, other):
        return Value(self.value or other.value)

    def __and__(self, other):
        return Value(self.value and other.value)

    def __repr__(self):
        return str(self.value)
    def replaceself(self,toreplace,withreplace):
        if type(self.value).__name__ == 'str':
            self.value=self.value.replace(toreplace.value,withreplace.value)
        else:
            raise RuntimeError("Can't apply replace function on other than string")
    def replacenew(self,toreplace,withreplace):
        if type(self.value).__name__ == 'str':
            return Value(self.value.replace(toreplace.value,withreplace.value))
        else:
            raise RuntimeError("Can't apply replace function on other than string")

class Dictionary:
    def __init__(self, data):
        self.data = data

    def get(self, key):
        return self.get(key, None)

    def set(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return str(self.data)

class Function:
    def __init__(self,name,args,body=None):
        self.name=name
        self.args=args
        self.body=body


class SymbolTable:
    def __init__(self, name, parent=None):
        self.symbols = {}
        self.name = name
        self.parent = parent

    def get(self, name):
        temp = self
        while temp != None:
            if name in list(temp.symbols.keys()):
                return temp.symbols[name]
            temp = temp.parent
        return None

    def set(self, name, value):
        temp = self
        while temp != None:
            if name in temp.symbols.keys():
                temp.symbols.update({name: value})
                return
            temp = temp.parent
        self.symbols.update({name: value})
        # if value ==  Value(None) and

    def remove(self, name):
        del self.symbols[name]