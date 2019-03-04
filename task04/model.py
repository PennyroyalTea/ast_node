#!/usr/bin/env python3

class Scope:
    def __init__(self, parent = None):
        pass


class Number:
    def __init__(self, value):
        pass
    def evaluate(self, scope):
        pass


class Function:
    def __init__(self, args, body):
        pass
    def evaluate(self, scope):
        pass


class FunctionDefinition:
    def __init__(self, name, function):
        pass
    def evaluate(self, scope):
        pass


class Conditional:
    def __init__(self, condition, if_true, if_false = None):
        pass
    def evaluate(self, scope)
        pass


class Print:
    def __init__(self, expr):
        pass
    def evaluate(self, scope):
        pass


class Read:
    def __init__(self, name):
        pass
    def evaluate(self, scope):
        pass


class FunctionCall:
    def __init__(self, fun_expr, args):
        pass
    def evaluate(self, scope):
        pass


class Reference:
    def __init__(self, name):
        pass
    def evaluate(self, scope):
        pass


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        pass
    def evaluate(self, scope):
        pass


class UnaryOperation:
    def __init__(self, op, expr):
        pass
    def evaluate(self, scope):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
