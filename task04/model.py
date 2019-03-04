#!/usr/bin/env python3

import abc


class ASTNode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, scope):
        """Evaluate a node and return its result"""


class Scope:
    def __init__(self, parent=None):
        pass


class Number(ASTNode):
    def __init__(self, value):
        pass


class Function(ASTNode):
    def __init__(self, args, body):
        pass


class FunctionDefinition(ASTNode):
    def __init__(self, name, function):
        pass


class Conditional(ASTNode):
    def __init__(self, condition, if_true, if_false=None):
        pass


class Print(ASTNode):
    def __init__(self, expr):
        pass


class Read(ASTNode):
    def __init__(self, name):
        pass


class FunctionCall(ASTNode):
    def __init__(self, fun_expr, args):
        pass


class Reference(ASTNode):
    def __init__(self, name):
        pass


class BinaryOperation(ASTNode):
    def __init__(self, lhs, op, rhs):
        pass


class UnaryOperation(ASTNode):
    def __init__(self, op, expr):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
