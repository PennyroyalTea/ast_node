#!/usr/bin/env python3

class Scope:
    def __init__(self, parent = None):
        pass


class Number:
    def __init__(self, value):
    def evaluate(self, scope):


class Function:
    def __init__(self, args, body):
    def evaluate(self, scope):


class FunctionDefinition:
    def __init__(self, name, function):
    def evaluate(self, scope):


class Conditional:
    def __init__(self, condition, if_true, if_false = None):
    def evaluate(self, scope)


class Print:
    def __init__(self, expr):
    def evaluate(self, scope):


class Read:
    def __init__(self, name):
    def evaluate(self, scope):


class FunctionCall:
    def __init__(self, fun_expr, args):
    def evaluate(self, scope):


class Reference:
    def __init__(self, name):
    def evaluate(self, scope):


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
    def evaluate(self, scope):


class UnaryOperation:
    def __init__(self, op, expr):
    def evaluate(self, scope):


def main():
    pass


if __name__ == '__main__':
    main()
