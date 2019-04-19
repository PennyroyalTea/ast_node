#!/usr/bin/env python3
import pytest
from model import *


if __name__ == "__main__":
    pytest.main()


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
