from model import ASTNodeVisitor


def fold_constants(program):
    pass


class ConstantFolder(ASTNodeVisitor):
    def visit_number(self, node):
        pass

    def visit_function(self, node):
        pass

    def visit_function_definition(self, node):
        pass

    def visit_conditional(self, node):
        pass

    def visit_print(self, node):
        pass

    def visit_read(self, node):
        pass

    def visit_function_call(self, node):
        pass

    def visit_reference(self, node):
        pass

    def visit_binary_operation(self, node):
        pass

    def visit_unary_operation(self, node):
        pass
