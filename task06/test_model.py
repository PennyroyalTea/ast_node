#!/usr/bin/env python3
import pytest
from model import *
from printer import *


def test_printer_end_to_end(capsys):
    pretty_print(FunctionDefinition('main', Function(['arg1'], [
        Read('x'),
        Print(Reference('x')),
        Conditional(
            BinaryOperation(Number(2), '==', Number(3)),
            [
                Conditional(Number(1), [], [])
            ],
            [
                FunctionCall(Reference('exit'), [
                    UnaryOperation('-', Reference('arg1'))
                ])
            ],
        ),
    ])))
    captured = capsys.readouterr()

    estimated = (
        "def main(arg1) {\n\t"
        "read x;\n\t"
        "print x;\n\t"
        "if (2 == 3) {\n\t\t"
        "if (1) {\n\t\t"
        "}\n\t"
        "} else {\n\t\t"
        "exit(-arg1);\n\t"
        "}\n"
        "}\n"
    )

    assert captured.out == estimated and not captured.err


def test_printer_conditional(capsys):
    pretty_print(Conditional(Number(42), [], []))

    captured = capsys.readouterr()
    estimated = 'if (42) {\n}\n'

    assert captured.out == estimated and not captured.err


def test_printer_func_definition(capsys):
    pretty_print(FunctionDefinition("foo", Function([], [])))

    captured = capsys.readouterr()
    estimated = 'def foo() {\n}\n'

    assert captured.out == estimated and not captured.err


def test_printer_print(capsys):
    pretty_print(Print(Number(42)))

    captured = capsys.readouterr()
    estimated = 'print 42;\n'

    assert captured.out == estimated and not captured.err


def test_printer_read(capsys):
    pretty_print(Read('x'))

    captured = capsys.readouterr()
    estimated = 'read x;\n'

    assert captured.out == estimated and not captured.err


def test_printer_number(capsys):
    pretty_print(Number(10))

    captured = capsys.readouterr()
    estimated = '10;\n'

    assert captured.out == estimated and not captured.err


def test_printer_reference(capsys):
    pretty_print(Reference('x'))

    captured = capsys.readouterr()
    estimated = 'x;\n'

    assert captured.out == estimated and not captured.err


def test_printer_binary_op(capsys):
    add = BinaryOperation(Number(2), '+', Number(3))
    mul = BinaryOperation(Number(1), '*', add)
    pretty_print(mul)

    captured = capsys.readouterr()
    estimated = '1 * (2 + 3);\n'

    assert captured.out == estimated and not captured.err


def test_printer_unary_op(capsys):
    pretty_print(UnaryOperation('-', Number(42)))

    captured = capsys.readouterr()
    estimated = '-42;\n'

    assert captured.out == estimated and not captured.err


def test_printer_function_call(capsys):
    pretty_print(FunctionCall(Reference('foo'),
                              [Number(1), Number(2), Number(3)]))

    captured = capsys.readouterr()
    estimated = 'foo(1, 2, 3);\n'

    assert captured.out == estimated and not captured.err


def test_construction():
    commands = [
        FunctionDefinition('fac', Function(['n'], [
            Conditional(
                BinaryOperation(Reference('n'), '==', Number(0)),
                [Number(1)],
                [
                    BinaryOperation(
                        Reference('n'),
                        '*',
                        FunctionCall(Reference('fac'), [
                            BinaryOperation(
                                Reference('n'),
                                '-',
                                Number(1)
                            )
                        ])
                    )
                ]
            )
        ])),
        Read('n'),
        Print(
            UnaryOperation('-',
                           FunctionCall(Reference('fac'), [Reference('n')]))
        )
    ]
    pretty_print_list(commands)


if __name__ == "__main__":
    pytest.main()
