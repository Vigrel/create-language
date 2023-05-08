from abc import ABC, abstractmethod
from typing import List
from SymbolTable import SymbolTable


class Node(ABC):
    def __init__(self, value, children) -> None:
        self.value: any = value
        self.children: List[Node] = children

    @abstractmethod
    def evaluate(self) -> any:
        return


class BinOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self) -> int:
        if self.value == "PLUS":
            return self.children[0].evaluate() + self.children[1].evaluate()
        if self.value == "MINUS":
            return self.children[0].evaluate() - self.children[1].evaluate()
        if self.value == "TIMES":
            return self.children[0].evaluate() * self.children[1].evaluate()
        if self.value == "DIVIDED":
            return self.children[0].evaluate() // self.children[1].evaluate()
        if self.value == "LT":
            return self.children[0].evaluate() < self.children[1].evaluate()
        if self.value == "GT":
            return self.children[0].evaluate() > self.children[1].evaluate()
        if self.value == "AND":
            return self.children[0].evaluate() and self.children[1].evaluate()
        if self.value == "OR":
            return self.children[0].evaluate() or self.children[1].evaluate()
        if self.value == "EQT":
            return self.children[0].evaluate() == self.children[1].evaluate()


class UnOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self) -> any:
        if self.value == "-":
            return -self.children[0].evaluate()
        return self.children[0].evaluate()


class IntVal(Node):
    def __init__(self, value: int) -> None:
        super().__init__(int(value), [])

    def evaluate(self) -> int:
        return self.value


class StrVal(Node):
    def __init__(self, value: int) -> None:
        super().__init__(str(value), [])

    def evaluate(self) -> int:
        return self.value


class NoOp(Node):
    def __init__(self) -> None:
        super().__init__(0, [])

    def evaluate(self) -> None:
        return None


class Print(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        print(self.children[0].evaluate())


class Identifier(Node):
    def __init__(self, value) -> None:
        super().__init__(value, [])

    def evaluate(self) -> int:
        return SymbolTable.getter(self.value)


class VarDec(Node):
    def __init__(self, value) -> None:
        super().__init__(value, [])

    def evaluate(self):
        SymbolTable.create(self.value)


class Assignment(Node):
    def __init__(self, value, children, func=False) -> None:
        super().__init__(value, children)
        self.func = func

    def evaluate(self):
        if self.func:
            SymbolTable.setter(self.value, self.children)
            return
        SymbolTable.setter(self.value, self.children[0].evaluate())


class Block(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        for child in self.children:
            child.evaluate()


class While(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        while self.children[0].evaluate():
            self.children[1].evaluate()


class If(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        if self.children[0].evaluate():
            return self.children[1].evaluate()
        if len(self.children) == 3:
            return self.children[2].evaluate()


class Function(Node):
    def __init__(self, parameters, children) -> None:
        super().__init__(0, children)
        # self.parameters = parameters

    def evaluate(self) -> None:
        local_symbols = SymbolTable()
        # for tkn in self.parameters:
        #     local_symbols.create(tkn.value)
        for child in self.children:
            child.evaluate()
