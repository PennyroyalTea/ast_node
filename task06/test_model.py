#!/usr/bin/env python3
import pytest
from model import *
from printer import *
from folder import *


def test_folder_binary_op_with_constants():
    cmd = BinaryOperation(Number(566), '>=', Number(239))
    assert fold_constants(cmd) == Number(1)


def test_folder_unary_constant():
    cmd = UnaryOperation('-', Number(12))
    assert fold_constants(cmd) == Number(-12)


def test_folder_binary_zero_left():
    cmd = BinaryOperation(Number(0), '*', Reference('HEY'))
    assert fold_constants(cmd) == Number(0)


def test_folder_binary_zero_right():
    cmd = BinaryOperation(Reference('x'), '*', Number(0))
    assert fold_constants(cmd) == Number(0)


def test_folder_binary_name_minus_name():
    cmd = BinaryOperation(Reference('bbb'), '-', Reference('bbb'))
    assert fold_constants(cmd) == Number(0)


def test_folder_and_printer_end_to_end(capsys):
    pretty_print(fold_constants(
        BinaryOperation(
            Number(10),
            '-',
            UnaryOperation(
                '-',
                BinaryOperation(
                    Number(3),
                    '+',
                    BinaryOperation(
                        Reference('x'),
                        '-',
                        Reference('x')
                    )
                )
            )
        )
    ))

    captured = capsys.readouterr()

    assert captured.out == '13;\n'


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
