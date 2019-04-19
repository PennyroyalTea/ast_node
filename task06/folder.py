from model import *


def fold_constants(program):
    folder = ConstantFolder()
    return program.accept(folder)


class ConstantFolder(ASTNodeVisitor):
    def visit_number(self, node):
        return Number(node.value)

    def visit_function(self, node):
        new_body = [cmd.accept(self) for cmd in node.body]
        return Function(node.args, new_body)

    def visit_function_definition(self, node):
        return FunctionDefinition(node.name, node.function.accept(self))

    def visit_conditional(self, node):
        condition = node.condition.accept(self)

        if_true = [cmd.accept(self) for cmd in node.if_true]
        if_false = [cmd.accept(self) for cmd in node.if_false or []]

        return Conditional(condition, if_true, if_false)

    def visit_print(self, node):
        return Print(node.expr.accept(self))

    def visit_read(self, node):
        return Read(node.name)

    def visit_function_call(self, node):
        fun_expr = node.fun_expr.accept(self)
        args = [arg.accept(self) for arg in node.args]
        return FunctionCall(fun_expr, args)

    def visit_reference(self, node):
        return Reference(node.name)

    def visit_binary_operation(self, node):
        lhs = node.lhs.accept(self)
        rhs = node.rhs.accept(self)
        op = node.op

        if isinstance(lhs, Reference) and isinstance(rhs, Reference) and \
                lhs.name == rhs.name and op == '-':
            return Number(0)

        if isinstance(lhs, Number) and op == '*' and lhs.value == 0:
            return Number(0)

        if isinstance(rhs, Number) and op == '*' and rhs.value == 0:
            return Number(0)

        if isinstance(lhs, Number) and isinstance(rhs, Number):
            res = BinaryOperation(lhs, op, rhs).evaluate(Scope())
            return res

        return BinaryOperation(lhs, op, rhs)

    def visit_unary_operation(self, node):
        expr = node.expr.accept(self)
        res = UnaryOperation(node.op, expr).evaluate(Scope())
        return res
