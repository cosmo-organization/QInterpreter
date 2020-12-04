import hashlib

def MyName(c=4, d=44):
    return c + c * c + d


def E(x):
    return [5, 5, 5, 5]


def Factorial(n):
    if n == 0:
        return 1
    else:
        return n * Factorial(n - 1)


def GiveMyName(yourname):
    return yourname


def SayHelloToUser(username):
    print("Hello User:", username)


def Max(n):
    if n == 0:
        return 1
    else:
        return n * Max(n - 1)


def Eval(exp):
    return eval(exp)


def Hash(data):
    return hashlib.sha3_512(data.encode('utf-8')).hexdigest()


def Execute(python_code):
    return exec(python_code)

def Something():
    print(BACKUP.self)
    print(ARRAY.index1)
def Login(username,password):
    print(DB.self)
    if username == DB.username and password == DB.password:
        return 'Logined Successfully'
    else:
        return 'Login Unsuccess'