#!/usr/bin/env python3
import abc


class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.scope = dict()

    def __getitem__(self, item):
        if item in self.scope:
            return self.scope[item]
        elif not self.parent:
            raise KeyError(item)
        else:
            return self.parent[item]

    def __setitem__(self, key, value):
        self.scope[key] = value


class ASTNode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, scope):
        """
        Запускает вычисление текущего узла синтаксического дерева
        в заданной области видимости и возвращает результат вычисления.
        """

    @abc.abstractmethod
    def accept(self, visitor):
        pass


class ASTNodeVisitor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def visit_number(self, node):
        pass

    @abc.abstractmethod
    def visit_function(self, node):
        pass

    @abc.abstractmethod
    def visit_function_definition(self, node):
        pass

    @abc.abstractmethod
    def visit_conditional(self, node):
        pass

    @abc.abstractmethod
    def visit_print(self, node):
        pass

    @abc.abstractmethod
    def visit_read(self, node):
        pass

    @abc.abstractmethod
    def visit_function_call(self, node):
        pass

    @abc.abstractmethod
    def visit_reference(self, node):
        pass

    @abc.abstractmethod
    def visit_binary_operation(self, node):
        pass

    @abc.abstractmethod
    def visit_unary_operation(self, node):
        pass


class Number(ASTNode):
    """
    Представляет собой константу или значение типа "целое число".

    Метод evaluate() всегда возвращает self.

    Number должен содержать поле value, которое будет хранить число,
    переданное в конструкторе.

    Также Number должен корректно работать с операторами ==, != и его должно
    быть можно положить в словарь в качестве ключа (см. специальные методы
    __eq__, __ne__, __hash__ — требуется реализовать две из них).
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.value == other.value

    def accept(self, visitor):
        visitor.visit_number(self)


class Function(ASTNode):
    """
    Представляет собой константу или значение типа "функция".

    Функция состоит из тела и списка имен аргументов.
    Тело функции — это список выражений, т. е. у каждого объекта в списке
    можно вызвать evaluate.
    Список имен аргументов - список имен формальных параметров функции.

    Аналогично Number, метод evaluate должен возвращать self.
    """
    def __init__(self, args=None, body=None):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self

    def accept(self, visitor):
        visitor.visit_function(self)


class FunctionDefinition(ASTNode):
    """
    Представляет собой определение функции, т. е. связывает некоторое
    имя с объектом типа Function.

    Результатом вычисления FunctionDefinition является побочный эффект -
    обновление текущего Scope,  т.е. в него добавляется новое значение типа
    Function под заданным именем, а возвращать evaluate должен саму функцию.
    """
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        visitor.visit_function_definition(self)


class Conditional(ASTNode):
    """
    Представляет ветвление в программе, т. е. if.

    condition - это некоторое выражение, результат вычисления которого
        обязательно является объектом типа Number.
    if_true и if_false - списки (возможно, пустые или равные None) выражений.

    Если результат вычисления condition - это объект Number, содержащий 0, то
    вычисляется if_false список, иначе if_true.

    Результатом вычисления всего Conditional является результат вычисления
    последнего элемента в соответствующем (if_true или if_false) списке.

    Если соответствующий список пуст или равен None, то возвращаемое значение
    остается на ваше усмотрение.
    """
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        condition_res = self.condition.evaluate(scope)

        branch = self.if_false if condition_res.value == 0 else self.if_true

        return_value = None
        for expr in (branch or []):
            return_value = expr.evaluate(scope)

        return return_value

    def accept(self, visitor):
        visitor.visit_conditional(self)


class Print(ASTNode):
    """
    Печатает значение выражения на отдельной строке.

    В методе evaluate вычисляется значение выражения expr, после чего
    на экран выводится число, хранящееся внутри результата вычисления (это
    гарантированно Number).

    Вывод завершается переходом на следующую строку (никаких дополнительных
    символов, лишнего форматирования, научных форматов, отступов и пр).

    Возвращаемое значение метода evаluate - объект типа Number, который был
    выведен.
    """
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res

    def accept(self, visitor):
        visitor.visit_print(self)


class Read(ASTNode):
    """
    Читает число из стандартного потока ввода и обновляет текущий Scope.

    Метод evaluate читает со стандартного потока ввода число (на отдельной
    строке) и добавляет в scope это число под именем name.

    evaluate должен возвращать объект типа Number, представляющий прочитанное
    число.

    Каждое входное число располагается на отдельной строке (никаких пустых
    строк и лишних символов не будет).
    """
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        num = Number(int(input()))
        scope[self.name] = num
        return num

    def accept(self, visitor):
        visitor.visit_read(self)


class FunctionCall(ASTNode):
    """
    Представляет вызов функции в программе.

    В результате вызова функции должен создаваться новый объект Scope,
    являющийся дочерним для текущего Scope (т.е. текущий Scope должен стать
    для него родителем). Новый Scope станет текущим Scope-ом при вычислении
    тела функции.

    Метод evaluate должен вычислить fun_expr и результатом этого вычисления
    будет объект типа Function (назовем его function). Кроме того, он должен
    вычислить все объекты в списке args слева направо,  результаты этих
    вычислений будут позиционными аргументами при вызове функции.

    Затем метод должен создать новый Scope (назовем его call_scope), родителем
    которого является scope. В call_scope должны быть добавлены результаты
    вычисления args, под именами, указанными в объекте Function, в
    соответствующем порядке.

    После этого нужно вычислить все выражения в теле function с использованием
    call_scope, результат вычисления последнего выражения будет результатом
    метода evaluate. Если результат вычисления последнего выражения
    неопределён, то возвращаемое значение остаётся на ваше усмотрение.
    """
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        local_scope = Scope(scope)
        args_list = [arg.evaluate(scope) for arg in self.args]

        for param_name, param in zip(function.args, args_list):
            local_scope[param_name] = param

        result = None
        for expr in function.body:
            result = expr.evaluate(local_scope)
        return result

    def accept(self, visitor):
        visitor.visit_function_call(self)


class Reference(ASTNode):
    """
    Представляет получение объекта (функции или переменной) по его имени.
    Метод evaluate должен найти в scope объект с именем name и вернуть его
    (см. подробнее про класс Scope).
    """
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        visitor.visit_reference(self)


class BinaryOperation(ASTNode):
    """
    Представляет бинарную операция над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции: '+', '-', '*', '/', '%', '==', '!=',
    '<', '>', '<=', '>=', '&&', '||'.

    lhs и rhs - левое и правое выражения соответственно.
    op - строка с обозначением оператора (все допустимые строки приведены
    выше).

    Метод evaluate должен вычислить значение lhs и rhs, и вернуть Number,
    хранящий значение соответствующей бинарной операции над результатами
    вычисления lhs и rhs.

    Для логических операций и операций сравнения считаем, что Number,
    хранящий 0, соответствует False, а остальные значения соответствуют True.
    Гарантируется, что lhs и rhs при вычислении дадут объект типа Number,
    т.е. не может получиться так, что вам придется сравнивать две функции.
    """
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        left = self.lhs.evaluate(scope)
        right = self.rhs.evaluate(scope)

        if self.op == '+':
            return Number(left.value + right.value)
        elif self.op == '-':
            return Number(left.value - right.value)
        elif self.op == '*':
            return Number(left.value * right.value)
        elif self.op == '/':
            return Number(left.value // right.value)
        elif self.op == '%':
            return Number(left.value % right.value)
        elif self.op == '==':
            return Number(int(left.value == right.value))
        elif self.op == '!=':
            return Number(int(left.value != right.value))
        elif self.op == '<':
            return Number(int(left.value < right.value))
        elif self.op == '>':
            return Number(int(left.value > right.value))
        elif self.op == '<=':
            return Number(int(left.value <= right.value))
        elif self.op == '>=':
            return Number(int(left.value >= right.value))
        elif self.op == '&&':
            return Number(int(bool(left.value) and bool(right.value)))
        elif self.op == '||':
            return Number(int(bool(left.value) or bool(right.value)))
        else:
            raise NotImplementedError

    def accept(self, visitor):
        visitor.visit_binary_operation(self)


class UnaryOperation(ASTNode):
    """
    Представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: '-', '!' (логическое отрицание, а не факториал).

    Метод evaluate должен вычислить expr, и вернуть Number, хранящий значение
    соответствующей унарной операции над результатом вычисления expr.
    Как и для BinaryOperation, Number, хранящий 0, считаем за False, а все
    остальные за True.
    """
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        if self.op == '-':
            return Number(res.value * -1)
        elif self.op == '!':
            return Number(int(not bool(res.value)))
        else:
            raise NotImplementedError

    def accept(self, visitor):
        visitor.visit_unary_operation(self)
