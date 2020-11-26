class Token:
    def __init__(self,value,type,line,col,file="<stdin>"):
        self.value=value
        self.type=type
        self.line=line
        self.col=col
        self.file=file
##########################
####### Expression #######
##########################
class BinOp:
    def __init__(self,left,op,right):
        self.left=left
        self.right=right
        self.op=op

class NumberExp:
    def __init__(self,tok):
        self.tok=tok

class UnaryExp:
    def __init__(self,fact):
        self.fact=fact

class VarExp:
    def __init__(self,tok):
        self.tok=tok

class VarAssignExp:
    def __init__(self,name,exp):
        self.name=name
        self.exp=exp

class MultiVarAssignExp:
    def __init__(self,listexp):
        self.listexp=listexp

class CompoundStatement:
    def __init__(self,statements):
        self.statements=statements

class Statements:
    def __init__(self,statements):
        self.statements=statements

class IfStatement:
    def __init__(self,condition,ifbody,elsebody,elseifbodies):
        self.ifbody=ifbody
        self.elsebody=elsebody
        self.elseifbodies=elseifbodies
        self.condition=condition

class ReturnStatement:
    def __init__(self,exp):
        self.exp=exp

class TupleExp:
    def __init__(self,args):
        self.args=args

class ListExp:
    def __init__(self,data):
        self.data=data

class StringExp:
    def __init__(self,tok):
        self.tok=tok
#########################
##### Values ############
#########################
class Value:
    def __init__(self,value):
        self.value=value
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
        return Value(self.value  or other.value)
    def __and__(self, other):
        return Value(self.value and other.value)
    def __repr__(self):
        return str(self.value)

class Dictionary:
    def __init__(self,data):
        self.data=data
    def get(self,key):
        return self.get(key,None)
    def set(self,key,value):
        self.data[key]=value
    def __repr__(self):
        return str(self.data)


class SymbolTable:
    def __init__(self,name,parent=None):
        self.symbols={}
        self.name=name
        self.parent=parent
    def get(self,name):
        temp=self
        while temp!=None:
            if name in list(temp.symbols.keys()):
                return temp.symbols[name]
            temp=temp.parent
        return None
    def set(self,name,value):
        temp=self
        while temp != None:
            if name in temp.symbols.keys():
                temp.symbols.update({name:value})
                return
            temp=temp.parent
        self.symbols.update({name:value})
        # if value ==  Value(None) and
    def remove(self,name):
        del self.symbols[name]