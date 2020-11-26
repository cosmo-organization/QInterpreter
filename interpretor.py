import re

from define import *


class Lexer:
    def __init__(self):
        self.tokens = []

    def tokenize(self, filename, lin_num, pre_include=[]):
        code = open(filename, 'r').read()
        for i in pre_include:
            code = 'Include(`' + i + '`);\n' + code
        rules = [
            ('COMMENT2', r'<#(\n|.)*#>'),  # COMMENTS
            ('COMMENT1', r'#.*'),  # COMMENTS
            ('PHP', r'Php'),  # PHP
            ('CONDITION', 'condition'),
            ('IMPORTKWD', r'Include\(`[^`]*`\);'),
            ('JS', r'Js'),  # JS
            ('CLINE', r'Line'),
            ('ID', 'Id'),
            ('CSPACE', r'Space'),
            ('PYTHON', r'Python'),  # PYTHON
            ('SESSION_KEY', r'Session.Key'),  # Server Segment
            ('COOKIE_KEY_TIME', r'Cookie.Key.Time'),  # Server Segment
            ('COOKIE_KEY', r'Cookie.Key'),  # Server Segment
            ('FILES_KEY', r'Files.Key'),  # Server Segment
            ('GET_KEY', r'Get.Key'),  # Server Segment
            ('POST_KEY', r'Post.Key'),  # Server Segment
            ('LOOP', r'Loop'),
            ('GLOBAL', r'Global'),  # &
            ('DIE', r'Die'),  # Die
            ('PRINT', r'Print'),  # Print
            ('RETURN', r'Return'),  # Return
            ('IF', r'If'),  # If
            ('OR', r'Or'),  # Or
            ('AND', r'And'),  # And
            ('ELSEIF', r'Elseif'),  # Elseif
            ('ELSE', r'Else'),  # Else
            ('CASE', r'case'),  # Case
            ('TIMES', r'Times'),  # Times
            ('ADD', r'Add'),  # Add
            ('AT', r'at'),  # at
            ('DELETE', r'Delete'),  # Delete
            ('LANG', r'Lang'),  # Lang
            ('REPLACE', r'Replace'),  # Replace
            ('WITH', r'With'),  # With
            ('POPULATE', r'Populate'),  # Populate
            ('FIND', r'Find'),  # Find
            ('XML', r'Xml'),  # Xml
            ('JSON', r'Json'),  # Json
            ('END', r'End'),  # End
            ('MIX', r'Mix'),  # Mix
            ('SPLIT', r'Split'),  # Split
            ('GET', r'Get'),  # Get
            ('TIME', r'Time'),  # Time
            ('LENGTH', r'Length'),  # Length
            ('LPAREN', r'\('),  # (
            ('RPAREN', r'\)'),  # )
            ('LBRACE', r'\{'),  # {
            ('RBRACE', r'\}'),  # }
            ('LBRACKET', r'\['),  # [
            ('RBRACKET', r'\]'),  # ]
            ('AMP', r'\&'),  # &
            ('LIST', r'List'),
            ('COMMA', r','),  # ,
            ('POINT', r'[.]'),  # .
            ('PCOMMA', r';'),  # ;
            ('COLON', r':'),  # :
            ('EQ', r'=='),  # ==
            ('NE', r'!='),  # !=
            ('LE', r'<='),  # <=
            ('GE', r'>='),  # >=
            ('ATTR', r'\='),  # =
            ('LT', r'<'),  # <
            ('GT', r'>'),  # >
            ('PLUS', r'\+'),  # +
            ('MINUS', r'-'),  # -
            ('MULT', r'\*'),  # *
            ('DIV', r'\/'),  # /
            ('VID', r'[a-z]\w*'),  # Variable IDENTIFIERS
            ('FID', r'[A-Z]\w*'),  # Function IDENTIFIERS
            ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),  # FLOAT
            ('INTEGER_CONST', r'\d(\d)*'),  # INT
            ('STRING_CONST1', r'`[^`]*`'),  # CONST STRING
            ('STRING_CONST2', r'"[^`]*"'),  # CONST STRING
            ('NEWLINE', r'\n'),  # NEW LINE
            ('SKIP', r'[ \t]+'),  # SPACE and TABS
            ('MISMATCH', r'.'),  # ANOTHER CHARACTER
            ('SPACE', '\s')
        ]
        importfound = False
        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        lin_start = 0
        col = 1
        for m in re.finditer(tokens_join, code):
            token_type = m.lastgroup
            token_lexeme = m.group(token_type)
            if token_type == 'NEWLINE':
                lin_start = m.end()
                lin_num = lin_num + 1
                col = 1
            elif token_type == 'SPACE':
                col += 1
            elif token_type == 'SKIP':
                col += 1
                continue
            elif token_type == 'MISMATCH':
                raise RuntimeError(
                    'Unexpected char "{}" from {} on col:{} line:{}'.format(token_lexeme, filename, col, lin_num))
            elif token_type == 'COMMENT1':
                for i in token_lexeme:
                    if i in [' \t']:
                        col += 1
                    elif i in ['\n']:
                        col = 0
                        lin_num += 1
            elif token_type == 'COMMENT2':
                for i in token_lexeme:
                    if i in [' \t']:
                        col += 1
                    elif i in ['\n']:
                        col = 0
                        lin_num += 1
            # '''('SESSION_KEY', r'Session.Key'),  # Server Segment
            # ('COOKIE_KEY_TIME', r'Cookie.Key.Time'),  # Server Segment
            # ('COOKIE_KEY', r'Cookie.Key'),  # Server Segment
            # ('FILES_KEY', r'Files.Key'),  # Server Segment
            # ('GET_KEY', r'Get.Key'),  # Server Segment
            # ('POST_KEY', r'Post.Key'),  # Server Segment'''
            elif token_type in ['SESSION_KEY', 'COOKIE_KEY_TIME', 'COOKIE_KEY', 'FILES_KEY', 'GET_KEY', 'POST_KEY']:
                col = (m.start() - lin_start) + 1
                self.tokens.append(Token(token_lexeme, 'VID', lin_num, col, filename))
            elif token_type == 'IMPORTKWD':
                col = (m.start() - lin_start) + 1
                toimport = token_lexeme.replace('Include', '').replace('`', '').replace('"', '').replace('(',
                                                                                                         '').replace(
                    ')', '').replace(';', '')
                l = Lexer()
                self.tokens += l.tokenize(toimport, 1)
            else:
                col = (m.start() - lin_start) + 1
                if token_type == 'STRING_CONST1' or token_type == 'STRING_CONST2':
                    token_lexeme = token_lexeme.replace('`', '').replace('"', '')
                self.tokens.append(Token(token_lexeme, token_type, lin_num, col, filename))
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.counter = -1
        self.c_t = None
        self.advance()

    def advance(self):
        self.counter += 1
        if self.counter == len(self.tokens):
            raise RuntimeError('Exception: EOF')
        self.c_t = self.tokens[self.counter]
        return self.c_t

    def eat(self, type):
        if self.c_t.type == type:
            data = self.c_t
            self.advance()
            return data
        else:
            raise RuntimeError("Expected '{}' but found '{}' line:{} col:{} in {}"
                               .format(type, self.c_t.value, self.c_t.line, self.c_t.col, self.c_t.file))

    def parse(self):
        self.tokens.append(Token('end of file', 'EOF', -1, -1))
        return self.compound()
    def compound(self):
        stmts=[]
        while self.c_t.type != 'EOF':
            if self.c_t.type == 'VID':
                temp = self.c_t
                vars = [temp]
                self.advance()
                while self.c_t.type == 'VID':
                    vars.append(self.eat('VID'))
                self.eat('ATTR')
                if len(vars) == 1:
                    ex=self.expr()
                    self.eat('PCOMMA')
                    stmts.append(VarAssignExp(temp,ex))
                else:
                    listexp = []
                    for i in vars:
                        listexp.append(VarAssignExp(i, self.expr()))
                    self.eat('PCOMMA')
                    stmts.append(MultiVarAssignExp(listexp))
            elif self.c_t.type == 'IF':
                self.advance()
                cd = self.expr()
                self.eat('COLON')
                self.eat('LBRACKET')
                stmt = self.compound()
                ex = IfStatement(cd,stmt,None,[])
                self.eat('RBRACKET')
                while self.c_t.type == 'ELSEIF':
                    self.advance()
                    pct = self.expr()
                    self.eat('COLON')
                    self.eat('LBRACKET')
                    stmt = self.compound()
                    ex.elseifbodies.append({'condition':pct,'body':stmt})
                    self.eat('RBRACKET')
                if self.c_t.type == 'ELSE':
                    self.advance()
                    self.eat('COLON')
                    self.eat('LBRACKET')
                    stmt = self.compound()
                    ex.elsebody=stmt
                    self.eat('RBRACKET')
                stmts.append(ex)
            elif self.c_t.type == 'ELSEIF':
                print("ElseIf Comming without if")
                raise RuntimeError("from {} Elseif without if at line:{} col:{}"
                                   .format(self.c_t.file, self.c_t.line, self.c_t.col))
            elif self.c_t.type == 'RETURN':
                self.advance()
                stmts.append(ReturnStatement(self.expr()))
                self.eat('PCOMMA')
            elif self.c_t.type == 'LIST':
                self.advance()
                stmts.append(ListExp(self.expr()))
                self.eat('PCOMMA')
            else:
                break
        return CompoundStatement(stmts)
    def statements(self):
        pass
    def expr(self):
        left = self.compr()
        temp = None
        while self.c_t.type in ['AND', 'OR']:
            temp = self.c_t
            self.advance()
            left = BinOp(left, temp, self.compr())
            # print("Logical\n",left.left,temp.value,left.right)
        return left

    def compr(self):
        left = self.arithmetic()
        temp = None
        while self.c_t.type in ['LT', 'GT', 'EQ', 'LTE', 'GTE', 'NE']:
            temp = self.c_t
            self.advance()
            left = BinOp(left, temp, self.arithmetic())
            # print("Comparision\n", left.left, temp.value, left.right)
        return left

    def arithmetic(self):
        left = self.term()
        temp = None
        while self.c_t.type in ['PLUS', 'MINUS']:
            temp = self.c_t
            self.advance()
            left = BinOp(left, temp, self.term())
            # print("Arithematics\n", left.left, temp.value, left.right)
        return left

    def term(self):
        left = self.factor()
        temp = None
        while self.c_t.type in ['DIV', 'MULT']:
            temp = self.c_t
            self.advance()
            left = BinOp(left, temp, self.factor())
            # print("Term-arithematics\n", left.left, temp.value, left.right)
        return left

    def factor(self):
        temp = self.c_t
        # print("Terminal and NonTerminal\n", temp.value)
        if temp.type in ['INTEGER_CONST', 'FLOAT_CONST']:
            self.advance()
            return NumberExp(temp)
        elif temp.type == 'LPAREN':
            self.advance()
            if self.c_t.type == 'VID' and self.tokens[self.counter+1].type == 'ATTR':
                args=self.argparser(sep='COMMA')
                self.eat('RPAREN')
                return TupleExp(args)
            temp = self.expr()
            self.eat('RPAREN')
            return temp
        elif temp.type == 'MINUS':
            self.advance()
            return UnaryExp(self.factor())
        elif temp.type == 'VID':
            self.advance()
            return VarExp(temp)
        elif temp.type == 'STRING_CONST1':
            self.advance()
            temp.value =temp.value.replace('`','')
            return StringExp(temp)
        elif temp.type == 'STRING_CONST2':
            self.advance()
            temp.value =temp.value.replace('"','')
            return StringExp(temp)
    def argparser(self,sep='AMP'):
        args={}
        while self.c_t.type == 'VID':
            temp=self.c_t
            self.advance()
            self.eat('ATTR')
            args.update({temp.value:self.expr()})
            if self.c_t.type == sep:
                self.eat(sep)
        return args

###############################
###############################
######### Interpreter #########
###############################
###############################
class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.symbol_table = None

    def visit(self, node, symbol_table=None):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, symbol_table)

    def visit_BinOp(self, node, symbol_table):
        left = self.visit(node.left, symbol_table)
        right = self.visit(node.right, symbol_table)
        result = None
        if node.op.value == '*':
            result = left * right
        elif node.op.value == '/':
            result = left / right
        elif node.op.value == '+':
            result = left + right
        elif node.op.value == '-':
            result = left - right
        elif node.op.value == '<':
            result = left < right
        elif node.op.value == '>':
            result = left > right
        elif node.op.value == '<=':
            result = left <= right
        elif node.op.value == '>=':
            result = left >= right
        elif node.op.value == '==':
            result = left == right
        elif node.op.value == '!=':
            result = left != right
        elif node.op.value == 'And':
            result = left & right
        elif node.op.value == 'Or':
            result = left | right
        return result

    def visit_UnaryExp(self, node, symbol_table):
        num = self.visit(node.fact)
        return num * Value(-1)
        # print('Unary visited:',num)

    def visit_NumberExp(self, node, symbol_table):
        if node.tok.type == 'INTEGER_CONST':
            return Value(int(node.tok.value))
        elif node.tok.type == 'FLOAT_CONST':
            return Value(float(node.tok.value))
        return Value(0)

    def visit_VarAssignExp(self,node,symbol_table):
        valname=node.name.value
        value=self.visit(node.exp,symbol_table)
        symbol_table.set(valname,value)

    def visit_MultiVarAssignExp(self,node,symbol_table):
        for i in node.listexp:
            self.visit(i,symbol_table)

    def visit_CompoundStatement(self,node,symbol_table):
        for i in node.statements:
            val=self.visit(i,symbol_table)
            if val:
                return val
    def no_visit_method(self, node, symbol_table):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_IfStatement(self,node,symbol_table):
        s_table=SymbolTable('If',symbol_table)
        elseifexecuted=False
        if self.visit(node.condition,symbol_table).value !=False:
            for v in node.ifbody.statements:
                val=self.visit(v,s_table)
                if val:
                    return val
        elif len(node.elseifbodies) > 0:
            for i in node.elseifbodies:
                if self.visit(i['condition'],symbol_table).value != False:
                    val=self.visit(i['body'],s_table)
                    elseifexecuted=True
                    if val:
                        return val
                    break
        if node.elsebody is not None and not elseifexecuted:
            val=self.visit(node.elsebody,s_table)
            elseifexecuted=False
            if val:
                return val

        return None
    def visit_VarExp(self,node,symbol_table):
        val= symbol_table.get(node.tok.value)
        if val:
            return val
        else:
            raise RuntimeError('Undefined variable {} at line:{} col:{} in {}'
                               .format(node.tok.value,node.tok.line,node.tok.col,node.tok.file))

    def visit_ReturnStatement(self,node,symbol_table):
        return self.visit(node.exp,symbol_table)

    def visit_TupleExp(self,node,symbol_table):
        details={}
        for i in node.args:
            details.update({i:self.visit(node.args[i],symbol_table)})
        return Dictionary(details)
    def visit_ListExp(self,node,symbol_table):
        value=self.visit(node.data,symbol_table)
        for i in value.data:
            symbol_table.set(i,value.data[i])
if __name__ == '__main__':
    # try:
        lexer = Lexer()
        data = lexer.tokenize('test.q', 1, [])
        p = Parser(data)
        tree = p.parse()
        global_symbol_table = SymbolTable('module')
        i = Interpreter(tree)
        i.visit(tree, global_symbol_table)
        print(global_symbol_table.name,global_symbol_table.symbols)
    # except Exception as ex:
    #     print("Runtime error",ex)