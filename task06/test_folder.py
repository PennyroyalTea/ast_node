import pytest
from model import *
from folder import *


if __name__ == "__main__":
    pytest.main()


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


def test_folder_end_to_end():
    folded = fold_constants(
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
    )

    assert folded == Number(13)


def test_folder_conditional(capsys):
    cmd = Conditional(
        BinaryOperation(
            Reference('x'),
            '-',
            Reference('x')
        ),
        [
            Print(
                UnaryOperation(
                    '!',
                    Number(239)
                )
            )
        ]
    )
    fold_constants(cmd).evaluate(Scope())

    captured = capsys.readouterr()
    assert captured.out == ''
