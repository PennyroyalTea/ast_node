from model import ASTNodeVisitor


def pretty_print_list(cmd_list):
    printer = PrettyPrinter()
    first = True
    for command in cmd_list:
        command.accept(printer)
        printer.newline()
    print(printer, end='')


def pretty_print(command):
    printer = PrettyPrinter()
    command.accept(printer)
    printer.newline()
    print(printer, end='')


class PrettyPrinter(ASTNodeVisitor):
    def __init__(self):
        self.result = ''
        self.indent = 0

    def __str__(self):
        return self.result

    def newline(self):
        if not self.result.endswith(('{', '}')):
            self.result += ';'
        self.result += '\n' + '\t' * self.indent

    def print_block(self, block):
        self.result += '{'
        self.indent += 1

        for command in block:
            self.newline()
            command.accept(self)

        self.indent -= 1
        self.newline()
        self.result += '}'

    def visit_number(self, node):
        self.result += str(node.value)

    def visit_function(self, node):
        self.print_block(node.body)

    def visit_function_definition(self, node):
        self.result += 'def {}({}) '.format(
            node.name,
            ', '.join(node.function.args)
        )
        node.function.accept(self)

    def visit_conditional(self, node):
        self.result += 'if ('
        node.condition.accept(self)
        self.result += ') '

        self.print_block(node.if_true)

        if node.if_false:
            self.result += ' else '
            self.print_block(node.if_false)

    def visit_print(self, node):
        self.result += 'print '
        node.expr.accept(self)

    def visit_read(self, node):
        self.result += 'read '
        self.result += node.name

    def visit_function_call(self, node):
        node.fun_expr.accept(self)
        self.result += '('
        is_first = True

        for arg in node.args:
            if not is_first:
                self.result += ', '
            is_first = True
            arg.accept(self)

        self.result += ')'

    def visit_reference(self, node):
        self.result += node.name

    def visit_binary_operation(self, node):
        left, right = node.need_braces()

        if left:
            self.result += '('
        node.lhs.accept(self)
        if left:
            self.result += ')'

        self.result += ' {} '.format(node.op)

        if right:
            self.result += '('
        node.rhs.accept(self)
        if right:
            self.result += ')'

    def visit_unary_operation(self, node):
        self.result += node.op

        braces = node.need_braces()

        if braces:
            self.result += '('

        node.expr.accept(self)

        if braces:
            self.result += ')'
