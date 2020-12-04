import copy
import re

from define import *
py_cmd=None
code='class Data:\n' \
     '\tdef __init__(self):\n'

def addmore(code,var,value):
    if type(value).__name__ == 'str':
        value='"'+value+'"'
    return code+'\t\tself.'+var+'='+str(value)+'\n'
def createvar(code,varname):
    exec(varname+'=Data()')
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
            ('IMPORTKWD', r'Include\(`[^`]*`\);'),
            ('JS', r'Js'),  # JS
            ('CLINE', r'Line'),
            ('ID', 'Id'),
            ('CONDITION', 'Condition'),
            ('JUMP', 'Jump'),
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
            ('STRING_CONST2', r'"[^"]*"'),  # CONST STRING
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
            elif token_lexeme.isupper() and token_lexeme.isalnum():
                col = (m.start() - lin_start) + 1
                token_type = 'GLOBAL_VID';
                self.tokens.append(Token(token_lexeme, token_type, lin_num, col, filename))
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
        return self.statements()

    def compound(self):
        stmts = []
        while self.c_t.type != 'EOF':
            if self.c_t.type == 'VID':
                temp = self.c_t
                self.advance()
                if self.c_t.type == 'POINT':
                    self.advance()
                    if self.c_t.type == 'REPLACE':
                        self.advance()
                        self.eat('LPAREN')
                        toreplace = self.expr()
                        self.eat('RPAREN')
                        self.eat('WITH')
                        self.eat('LPAREN')
                        withreplace = self.expr()
                        self.eat('RPAREN')
                        self.eat('PCOMMA')
                        stmts.append(SelfReplaceExp(temp, toreplace, withreplace))
                    elif self.c_t.type == 'VID':
                        subvar = self.c_t
                        self.advance()
                        self.eat('ATTR')
                        exp = self.expr()
                        self.eat('PCOMMA')
                        stmts.append(AssignSubVarExp(temp, subvar, exp))
                else:
                    vars = [temp]
                    while self.c_t.type == 'VID':
                        vars.append(self.eat('VID'))
                    self.eat('ATTR')
                    if len(vars) == 1:
                        ex = self.expr()
                        self.eat('PCOMMA')
                        stmts.append(VarAssignExp(temp, ex))
                    else:
                        listexp = []
                        for i in vars:
                            listexp.append(VarAssignExp(i, self.expr()))
                        self.eat('PCOMMA')
                        stmts.append(MultiVarAssignExp(listexp))
            elif self.c_t.type == 'PRINT':
                self.advance()
                self.eat('LPAREN')
                stmts.append(PrintStatement(self.argparserex(sep='AMP')))
                self.eat('RPAREN')
                self.eat('PCOMMA')
            elif self.c_t.type == 'GLOBAL':
                self.advance()
                var = self.eat('VID')
                self.eat('ATTR')
                exp = self.expr()
                self.eat('PCOMMA')
                stmts.append(GlobalExp(VarAssignExp(var, exp)))
            elif self.c_t.type == 'LOOP':
                self.advance()
                self.eat('LPAREN')
                vid = self.eat('VID')
                self.eat('RPAREN')
                timeexp = None
                conditionexp = None
                body = None
                if self.c_t.type == 'TIMES':
                    self.advance()
                    self.eat('LPAREN')
                    timeexp = self.expr()
                    self.eat('RPAREN')
                if self.c_t.type == 'CONDITION':
                    self.advance()
                    self.eat('LPAREN')
                    conditionexp = self.expr()
                    self.eat('RPAREN')
                self.eat('COLON')
                self.eat('LBRACKET')
                body = self.compound()
                self.eat('RBRACKET')
                stmts.append(LoopStatement(vid, conditionexp, timeexp, body))
            elif self.c_t.type == 'IF':
                self.advance()
                cd = self.expr()
                self.eat('COLON')
                self.eat('LBRACKET')
                stmt = self.compound()
                ex = IfStatement(cd, stmt, None, [])
                self.eat('RBRACKET')
                while self.c_t.type == 'ELSEIF':
                    self.advance()
                    pct = self.expr()
                    self.eat('COLON')
                    self.eat('LBRACKET')
                    stmt = self.compound()
                    ex.elseifbodies.append({'condition': pct, 'body': stmt})
                    self.eat('RBRACKET')
                if self.c_t.type == 'ELSE':
                    self.advance()
                    self.eat('COLON')
                    self.eat('LBRACKET')
                    stmt = self.compound()
                    ex.elsebody = stmt
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
            elif self.c_t.type == 'GLOBAL_VID':
                temp = self.c_t
                self.advance()
                if self.c_t.type == 'POINT':
                    self.advance()
                    subvar = self.eat('VID')
                    self.eat('ATTR')
                    exp = self.expr()
                    self.eat('PCOMMA')
                    stmts.append(AssignDictExp(temp, subvar, exp))
                else:
                    self.eat('ATTR')
                    exp = self.expr()
                    self.eat('PCOMMA')
                    stmts.append(AssignDictExp(temp, Token('$', temp.type, temp.line, temp.col, temp.file), exp))

            elif self.c_t.type == 'LIST':
                self.advance()
                stmts.append(ListExp(self.expr()))
                self.eat('PCOMMA')
            elif self.c_t.type == 'FID':
                temp = self.c_t
                if temp.value in list(functions.keys()):
                    stmts.append(self.expr())
                    self.eat('PCOMMA')
                elif temp.value in list(py_functions.keys()):
                    self.c_t.type = 'PFID'
                    stmts.append(self.expr())
                    self.eat('PCOMMA')
            else:
                break
        return CompoundStatement(stmts)

    def statements(self):
        stmts = []
        while self.c_t.type != 'EOF':
            if self.c_t.type == 'VID':
                temp = self.c_t
                self.advance()
                if self.c_t.type == 'POINT':
                    self.advance()
                    if self.c_t.type == 'REPLACE':
                        self.advance()
                        self.eat('LPAREN')
                        toreplace = self.expr()
                        self.eat('RPAREN')
                        self.eat('WITH')
                        self.eat('LPAREN')
                        withreplace = self.expr()
                        self.eat('RPAREN')
                        self.eat('PCOMMA')
                        stmts.append(SelfReplaceExp(temp, toreplace, withreplace))
                    elif self.c_t.type == 'VID':
                        subvar = self.c_t
                        self.advance()
                        self.eat('ATTR')
                        exp = self.expr()
                        self.eat('PCOMMA')
                        stmts.append(AssignSubVarExp(temp, subvar, exp))
                else:
                    vars = [temp]
                    while self.c_t.type == 'VID':
                        vars.append(self.eat('VID'))
                    self.eat('ATTR')
                    if len(vars) == 1:
                        ex = self.expr()
                        self.eat('PCOMMA')
                        stmts.append(VarAssignExp(temp, ex))
                    else:
                        listexp = []
                        for i in vars:
                            listexp.append(VarAssignExp(i, self.expr()))
                        self.eat('PCOMMA')
                        stmts.append(MultiVarAssignExp(listexp))
            elif self.c_t.type == 'GLOBAL_VID':
                temp = self.c_t
                self.advance()
                data = {}
                dictexp = DictExp(temp, None, data)
                if temp.file == 'configure.q':
                    self.eat('LPAREN')
                    ep = self.expr()
                    self.eat('RPAREN')
                    dictexp.exp = ep
                    while self.c_t.type == 'VID':
                        temp = self.c_t
                        self.advance()
                        self.eat('LPAREN')
                        exp = self.expr()
                        self.eat('RPAREN')
                        dictexp.table.update({temp: exp})
                    self.eat('PCOMMA')
                    stmts.append(dictexp)
                elif self.c_t.type == 'POINT':
                    self.advance()
                    subvar = self.eat('VID')
                    self.eat('ATTR')
                    exp = self.expr()
                    self.eat('PCOMMA')
                    stmts.append(AssignDictExp(temp, subvar, exp))
                else:
                    self.eat('ATTR')
                    exp = self.expr()
                    self.eat('PCOMMA')
                    stmts.append(AssignDictExp(temp, Token('$', temp.type, temp.line, temp.col, temp.file), exp))

            elif self.c_t.type == 'PRINT':
                self.advance()
                self.eat('LPAREN')
                stmts.append(PrintStatement(self.argparserex(sep='AMP')))
                self.eat('RPAREN')
                self.eat('PCOMMA')
            elif self.c_t.type == 'GLOBAL':
                self.advance()
                var = self.eat('VID')
                self.eat('ATTR')
                exp = self.expr()
                self.eat('PCOMMA')
                stmts.append(GlobalExp(VarAssignExp(var, exp)))
            elif self.c_t.type == 'IF':
                self.advance()
                cd = self.expr()
                self.eat('COLON')
                self.eat('LBRACKET')
                stmt = self.compound()
                ex = IfStatement(cd, stmt, None, [])
                self.eat('RBRACKET')
                while self.c_t.type == 'ELSEIF':
                    self.advance()
                    pct = self.expr()
                    self.eat('COLON')
                    self.eat('LBRACKET')
                    stmt = self.compound()
                    ex.elseifbodies.append({'condition': pct, 'body': stmt})
                    self.eat('RBRACKET')
                if self.c_t.type == 'ELSE':
                    self.advance()
                    self.eat('COLON')
                    self.eat('LBRACKET')
                    stmt = self.compound()
                    ex.elsebody = stmt
                    self.eat('RBRACKET')
                stmts.append(ex)
            elif self.c_t.type == 'ELSEIF':
                print("ElseIf Comming without if")
                raise RuntimeError("from {} Elseif without if at line:{} col:{}"
                                   .format(self.c_t.file, self.c_t.line, self.c_t.col))
            elif self.c_t.type == 'LIST':
                self.advance()
                stmts.append(ListExp(self.expr()))
                self.eat('PCOMMA')
            elif self.c_t.type == 'ID':
                self.advance()
                self.eat('LPAREN')
                data = self.expr()
                self.eat('RPAREN')
                self.eat('PCOMMA')
                stmts.append(IdExp(data))
            elif self.c_t.type == 'JUMP':
                self.advance()
                self.eat('LPAREN')
                idexp = self.expr()
                timeexp = None
                conditionexp = None
                self.eat('RPAREN')
                if self.c_t.type == 'TIMES':
                    self.advance()
                    self.eat('LPAREN')
                    timeexp = self.expr()
                    self.eat('RPAREN')
                if self.c_t.type == 'CONDITION':
                    self.advance()
                    self.eat('LPAREN')
                    conditionexp = self.expr()
                    self.eat('RPAREN')
                self.eat('PCOMMA')
                stmts.append(JumpExp(idexp, timeexp, conditionexp))
            elif self.c_t.type == 'LOOP':
                self.advance()
                self.eat('LPAREN')
                vid = self.eat('VID')
                self.eat('RPAREN')
                timeexp = None
                conditionexp = None
                body = None
                if self.c_t.type == 'TIMES':
                    self.advance()
                    self.eat('LPAREN')
                    timeexp = self.expr()
                    self.eat('RPAREN')
                if self.c_t.type == 'CONDITION':
                    self.advance()
                    self.eat('LPAREN')
                    conditionexp = self.expr()
                    self.eat('RPAREN')
                self.eat('COLON')
                self.eat('LBRACKET')
                body = self.compound()
                self.eat('RBRACKET')
                stmts.append(LoopStatement(vid, conditionexp, timeexp, body))
            elif self.c_t.type == 'FID':
                temp = self.c_t
                if temp.value in list(functions.keys()):
                    stmts.append(self.expr())
                    self.eat('PCOMMA')
                elif temp.value in list(py_functions.keys()):
                    self.c_t.type = 'PFID'
                    stmts.append(self.expr())
                    self.eat('PCOMMA')
                else:
                    self.advance()
                    self.eat('LPAREN')
                    arguments = self.args()
                    self.eat('RPAREN')
                    if self.c_t.type == 'PCOMMA':
                        self.advance()
                        stmts.append(PyFuncExp(temp, arguments))
                        py_functions.update({temp.value: 0})
                    elif self.c_t.type == 'COLON':
                        self.advance()
                        self.eat('LBRACKET')
                        functions.update({temp.value: 0})
                        body = self.compound()
                        self.eat('RBRACKET')
                        self.eat('PCOMMA')
                        stmts.append(FuncExp(temp, arguments, body))
            else:
                break
        return Statements(stmts)

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
        while self.c_t.type in ['LT', 'GT', 'EQ', 'LE', 'GE', 'NE']:
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
            if self.c_t.type == 'VID' and self.tokens[self.counter + 1].type == 'ATTR':
                args = self.argparser(sep='COMMA')
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
            if self.c_t.type == 'POINT':
                self.advance()
                if self.c_t.type == 'REPLACE':
                    self.advance()
                    self.eat('LPAREN')
                    toreplace = self.expr()
                    self.eat('RPAREN')
                    self.eat('WITH')
                    self.eat('LPAREN')
                    withreplace = self.expr()
                    self.eat('RPAREN')
                    return AssignReplaceExp(temp, toreplace, withreplace)
                elif self.c_t.type == 'VID':
                    subvar = self.c_t
                    self.advance()
                    return AccessSubVarExp(temp, subvar)
            return VarExp(temp)
        elif temp.type == 'STRING_CONST1':
            self.advance()
            temp.value = temp.value.replace('`', '')
            return StringExp(temp)
        elif temp.type == 'STRING_CONST2':
            self.advance()
            temp.value = temp.value.replace('"', '')
            return StringExp(temp)
        elif temp.type == 'CLINE':
            self.advance()
            if self.c_t.type == 'LPAREN':
                self.advance()
                data = LineExp(self.expr())
                self.eat('RPAREN')
                return data
            else:
                return LineExp(None)
        elif temp.type == 'CSPACE':
            self.advance()
            if self.c_t.type == 'LPAREN':
                self.advance()
                data = SpaceExp(self.expr())
                self.eat('RPAREN')
                return data
            else:
                return SpaceExp(None)
        elif temp.type == 'FID':
            if temp.value in py_functions:
                self.advance()
                self.eat('LPAREN')
                args = self.argparserex()
                self.eat('RPAREN')
                keyval = {}
                while self.c_t.type == 'VID':
                    t = self.c_t
                    self.advance()
                    self.eat('LPAREN')
                    exp = self.expr()
                    self.eat('RPAREN')
                    keyval.update({t.value: exp})
                keyval.update({'$': args})
                return FuncCallExp(temp, keyval, typecall='PFID')
            self.advance()
            self.eat('LPAREN')
            arg = self.argparserex()
            self.eat('RPAREN')
            return FuncCallExp(temp, arg, typecall='FID')
        elif temp.type == 'PFID':
            self.advance()
            self.eat('LPAREN')
            args = self.argparserex()
            self.eat('RPAREN')
            keyval = {}
            while self.c_t.type == 'VID':
                t = self.c_t
                self.advance()
                self.eat('LPAREN')
                exp = self.expr()
                self.eat('RPAREN')
                keyval.update({t.value: exp})
            keyval.update({'$': args})
            return FuncCallExp(temp, keyval, typecall='PFID')
        elif temp.type == 'GLOBAL_VID':
            self.advance()
            if self.c_t.type == 'POINT':
                self.advance()
                subvar = self.eat('VID')
                return DictAccessExp(temp, subvar)
            else:
                return DictAccessExp(temp, Token('$', temp.type, temp.line, temp.col, temp.file))
        else:
            pass

    def argparser(self, sep='AMP', outer=False):
        args = {}
        while self.c_t.type == 'VID':
            temp = self.c_t
            self.advance()
            self.eat('ATTR')
            args.update({temp.value: self.expr()})
            if self.c_t.type == sep:
                self.eat(sep)
        return args

    def args(self, sep='AMP'):
        arguments = {}
        while self.c_t.type == 'VID':
            temp = self.c_t
            for a in arguments:
                if temp.value in a:
                    raise RuntimeError("from {} duplicate args {} at line:{} col:{}"
                                       .format(temp.file, temp.value, temp.line, temp.col))
            self.advance()
            if self.c_t.type == 'ATTR':
                self.advance()
                arguments.update({temp.value: self.expr()})
                if self.c_t.type == sep: self.eat(sep)
            else:
                arguments.update({temp.value: NumberExp(Token(0, 'CONST_INT', temp.line, temp.col, temp.file))})
                if self.c_t.type == sep: self.eat(sep)
        return arguments

    def argparserex(self, sep='AMP'):
        list = []
        while self.c_t.type == 'VID' or self.c_t.type == 'INTEGER_CONST' or \
                self.c_t.type == 'FLOAT_CONST' or self.c_t.type == 'STRING_CONST1' or \
                self.c_t.type == 'STRING_CONST2' or self.c_t.type == 'CLINE' or self.c_t.type == 'CSPACE' \
                or self.c_t.type == 'FID' or self.c_t.type == 'GLOBAL_VID':
            if self.c_t.value in py_functions:
                self.c_t.type = 'PFID'
            list.append(self.expr())
            if self.c_t.type == sep:
                self.eat(sep)
        return list


###############################
###############################
######### Interpreter #########
###############################
###############################
global_statement = None
py_functions = {}
functions = {}


class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.symbol_table = None
        self.loopstack = []

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

    def visit_VarAssignExp(self, node, symbol_table):
        valname = node.name.value
        value = self.visit(node.exp, symbol_table)
        symbol_table.set(valname, value)

    def visit_MultiVarAssignExp(self, node, symbol_table):
        for i in node.listexp:
            self.visit(i, symbol_table)

    def visit_CompoundStatement(self, node, symbol_table):
        while node.havenext():
            val = self.visit(node.next(), symbol_table)
            if val:
                return val

    def no_visit_method(self, node, symbol_table):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_IfStatement(self, node, symbol_table):
        s_table = SymbolTable('If', symbol_table)
        elseifexecuted = False
        if self.visit(node.condition, symbol_table).value != False:
            for v in node.ifbody.statements:
                val = self.visit(v, s_table)
                if val:
                    return val
        elif len(node.elseifbodies) > 0:
            for i in node.elseifbodies:
                if self.visit(i['condition'], symbol_table).value != False:
                    val = self.visit(i['body'], s_table)
                    elseifexecuted = True
                    if val:
                        return val
                    break
        elif node.elsebody is not None and not elseifexecuted:
            elseifexecuted = False
            for i in node.elsebody.statements:
                val = self.visit(i, s_table)
                if val:
                    return val

        return None

    def visit_VarExp(self, node, symbol_table):
        val = symbol_table.get(node.tok.value)
        if val:
            return val
        else:
            raise RuntimeError('Undefined variable "{}" at line:{} col:{} in {} from {}'
                               .format(node.tok.value, node.tok.line, node.tok.col, node.tok.file, symbol_table.name))

    def visit_ReturnStatement(self, node, symbol_table):
        return self.visit(node.exp, symbol_table)

    def visit_TupleExp(self, node, symbol_table):
        details = {}
        for i in node.args:
            details.update({i: self.visit(node.args[i], symbol_table)})
        return Dictionary(details)

    def visit_ListExp(self, node, symbol_table):
        value = self.visit(node.data, symbol_table)
        for i in value.data:
            symbol_table.set(i, value.data[i])

    def visit_StringExp(self, node, symbol_table):
        return Value(node.tok.value)

    def visit_PrintStatement(self, node, symbol_table):
        for i in node.args:
            print(self.visit(i, symbol_table), end='')

    def visit_SpaceExp(self, node, symbol_table):
        if node.exp is not None:
            n = self.visit(node.exp, symbol_table)
            data = ""
            for i in range(n.value):
                data += " "
            return Value(data)
        else:
            return Value(" ")

    def visit_LineExp(self, node, symbol_table):
        if node.exp is not None:
            n = self.visit(node.exp, symbol_table)
            data = ""
            for i in range(n.value):
                data += "\n"
            return Value(data)
        else:
            return Value("\n")

    def visit_Statements(self, node, symbol_table):
        while node.havenext():
            self.visit(node.next(), symbol_table)

    def visit_IdExp(self, node, symbol_table):
        value = self.visit(node.exp, symbol_table)
        global_symbol_table.set(value.value, Value(global_statement.getjump()))

    def visit_JumpExp(self, node, symbol_table):
        tojump = self.visit(node.idexp, symbol_table).value
        v = global_symbol_table.get(tojump).value
        condition = node.conditionexp
        times = None if node.timeexp is None else self.visit(node.timeexp, symbol_table).value
        if condition is not None and times is not None:
            while times > node.counter and self.visit(condition, symbol_table).value == True:
                for i in range(v, global_statement.getjump() - 1):
                    # print(global_statement.statements[i])
                    self.visit(global_statement.statements[i], symbol_table)
                node.counter += 1
            node.counter = 0
        elif condition is not None:
            while self.visit(condition, symbol_table).value == True:
                for i in range(v, global_statement.getjump() - 1):
                    self.visit(global_statement.statements[i], symbol_table)
        elif times is not None:
            while times > node.counter:
                for i in range(v, global_statement.getjump() - 1):
                    self.visit(global_statement.statements[i], symbol_table)
                node.counter += 1
            node.counter = 0
        elif times is None and condition is None:
            while True:
                for i in range(v, global_statement.getjump() - 1):
                    self.visit(global_statement.statements[i], symbol_table)

    def visit_GlobalExp(self, node, symbol_table):
        self.visit(node.exp, global_symbol_table)

    def visit_LoopStatement(self, node, symbol_table):
        stm = SymbolTable('LOOP', symbol_table)
        var = node.var.value
        if node.condition is not None and node.times is not None:
            value = symbol_table.get(var)
            if type(value).__name__ == 'Value':
                stm.set('key', Value(var))
                stm.set('value', value)
                i = 0
                while i < self.visit(node.times, stm).value and self.visit(node.condition, stm).value == True:
                    i += 1
                    for j in node.body.statements:
                        val = self.visit(j, stm)
                        if val:
                            return val
            elif type(value).__name__ == 'Dictionary':
                keys = list(value.data.keys())
                i = 0
                k = 0
                while i < self.visit(node.times, stm).value and self.visit(node.condition, stm).value == True:
                    i += 1
                    if k == len(keys): k = 0
                    key = keys[k]
                    k += 1
                    stm.set('key', Value(key))
                    stm.set('value', value.data[key])
                    for j in node.body.statements:
                        val = self.visit(j, stm)
                        if val:
                            return val
        elif node.condition is not None:
            value = symbol_table.get(var)
            if type(value).__name__ == 'Value':
                stm.set('key', Value(var))
                stm.set('value', value)
                while self.visit(node.condition, stm).value == True:
                    for j in node.body.statements:
                        val = self.visit(j, stm)
                        if val:
                            return val
            elif type(value).__name__ == 'Dictionary':
                keys = list(value.data.keys())
                k = 0
                while self.visit(node.condition, stm).value == True:
                    if k == len(keys): k = 0
                    key = keys[k]
                    k += 1
                    stm.set('key', Value(key))
                    stm.set('value', value.data[key])
                    for j in node.body.statements:
                        val = self.visit(j, stm)
                        if val:
                            return val
        elif node.times is not None:
            value = symbol_table.get(var)
            if type(value).__name__ == 'Value':
                stm.set('key', Value(var))
                stm.set('value', value)
                i = 0
                while i < self.visit(node.times, stm).value:
                    i += 1
                    for j in node.body.statements:
                        val = self.visit(j, stm)
                        if val:
                            return val
            elif type(value).__name__ == 'Dictionary':
                keys = list(value.data.keys())
                i = 0
                k = 0
                while i < self.visit(node.times, stm).value:
                    i += 1
                    if k == len(keys): k = 0
                    key = keys[k]
                    k += 1
                    stm.set('key', Value(key))
                    stm.set('value', value.data[key])
                    for j in node.body.statements:
                        val = self.visit(j, stm)
                        if val:
                            return val
        elif node.condition is None and node.times is None:
            value = symbol_table.get(var)
            if type(value).__name__ == 'Value':
                stm.set('key', Value(var))
                stm.set('value', value)
                for i in node.body.statements:
                    val = self.visit(i, stm)
                    if val:
                        return val
            elif type(value).__name__ == 'Dictionary':
                for i in list(value.data.keys()):
                    stm.set('key', Value(i))
                    stm.set('value', value.data[i])
                    for j in node.body.statements:
                        val = self.visit(j, stm)
                        if val:
                            return val
        # print("Aesop")

    def visit_FuncExp(self, node, symbol_table):
        f = Function(node.name, node.args, node.body)
        global_symbol_table.set(node.name.value, f)

    def visit_PyFuncExp(self, node, symbol_table):
        f = Function(node.name, node.args, None)
        global_symbol_table.set(node.name.value, f)

    def visit_FuncCallExp(self, node, symbol_table):
        if node.typecall == 'FID':
            stm = SymbolTable(node.name.value, symbol_table)
            func = global_symbol_table.get(node.name.value)
            if len(func.args) < len(node.args):
                raise RuntimeError("Too many argument supplied function:{} at line:{} col:{} in file:{}"
                                   .format(func.name.value, node.name.line, node.name.col, node.name.file))
            evaluated = []
            for i in func.args:
                evaluated.append(self.visit(func.args[i], symbol_table))
            i = 0
            newevaluated = []
            for j in node.args:
                newevaluated.append(self.visit(j, symbol_table))
            for j in newevaluated:
                evaluated[i] = j
                i += 1
            i = 0
            for j in func.args:
                stm.symbols.update({j: evaluated[i]})
                i += 1
            for i in func.body.statements:
                val = self.visit(i, stm)
                if val:
                    return val
        elif node.typecall == 'PFID':
            stm = SymbolTable(node.name.value, symbol_table)
            args = copy.copy(node.args)
            all = args.pop('$')
            f = global_symbol_table.get(node.name.value)
            if len(f.args) < len(all) or len(f.args) < len(args):
                raise RuntimeError('Too many argument supplied function:{} line:{} col:{} in {}'
                                   .format(node.name.value, node.name.line, node.name.col, node.name.file))
            evaluated = {}
            for i in f.args:
                evaluated.update({i: self.visit(f.args[i], symbol_table)})
            k = 0
            keys = list(evaluated.keys())
            for i in all:
                evaluated.update({keys[k]: self.visit(i, symbol_table)})
                k += 1
            for i in args:
                evaluated.update({i: self.visit(args[i], symbol_table)})
            argument_pass_str = ""
            for i in evaluated:
                argument_pass_str += i + "="
                if type(evaluated[i].value).__name__ == 'str':
                    argument_pass_str += '"' + evaluated[i].value + '",'
                else:
                    argument_pass_str += str(evaluated[i].value) + ","
            argument_pass_str = argument_pass_str[:len(argument_pass_str) - 1]
            pyzf = "" + f.name.value + "(" + argument_pass_str + ")"
            val = eval(pyzf)
            if val != None:
                return Value(val)

    def visit_SelfReplaceExp(self, node, symbol_table):
        data = symbol_table.get(node.var.value)
        data.replaceself(self.visit(node.toreplace, symbol_table), self.visit(node.withreplace, symbol_table))

    def visit_AssignReplaceExp(self, node, symbol_table):
        return symbol_table.get(node.var.value).replacenew(self.visit(node.toreplace, symbol_table),
                                                           self.visit(node.withreplace, symbol_table))

    def visit_DictExp(self, node, symbol_table):
        template=code
        data = {}
        selfvalue = self.visit(node.exp, global_symbol_table)
        data.update({'$': selfvalue})
        template=addmore(template,'self',selfvalue.value)
        global_symbol_table.set(node.var.value, Dictionary(data))
        for i in node.table:
            val=self.visit(node.table[i])
            template=addmore(template,i.value,val.value)
            data.update({i.value: val})
        exec(template)
        globals().update({node.var.value:eval('Data()')})

    def visit_DictAccessExp(self, node, symbol_table):
        data = global_symbol_table.get(node.var.value)
        return data.get(node.subvar.value)

    def visit_AssignDictExp(self, node, symbol_table):
        template = code
        data = global_symbol_table.get(node.var.value)
        data.set(node.subvar.value, self.visit(node.exp, global_symbol_table))
        for i in data.data:
            if i == node.subvar.value:
                i=i.replace('$','self')
                template=addmore(template,i,self.visit(node.exp,global_symbol_table).value)
            else:
                if i == '$':
                    template=addmore(template,'self',data.get(i).value)
                else:
                    template=addmore(template,i,data.get(i).value)
        exec(template)
        globals().update({node.var.value: eval('Data()')})

    def visit_AssignSubVarExp(self, node, symbol_table):
        symbol_table.get(node.var.value).set(node.subvar.value, self.visit(node.exp, symbol_table))

    def visit_AccessSubVarExp(self, node, symbol_table):
        return symbol_table.get(node.var.value).get(node.subvar.value)


import sys

if __name__ == '__main__':
    # try:
        sys.setrecursionlimit(10000)
        lexer = Lexer()
        data = lexer.tokenize('test.q', 1, ['configure.q', 'command.q'])
        p = Parser(data)
        tree = p.parse()
        global_symbol_table = SymbolTable('module')
        source=open('py_command.py').read()
        exec(source)
        global_statement = tree
        i = Interpreter(tree)
        i.visit(tree, global_symbol_table)
    # except Exception as ex:
    #     print('\n', ex)