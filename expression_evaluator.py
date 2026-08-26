"""Safe arithmetic expression handling for the calculator."""

import ast
import operator
from typing import Final, Callable


Number = int | float
Operator = Callable[..., Number]
OPERATORS: Final[dict[type[ast.operator], Operator]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


class ExpressionEvaluator:
    """Builds calculator expressions and evaluates only approved AST nodes."""

    def __init__(self) -> None:
        """Start with an empty expression, matching the original calculator."""
        self.expression = ""

    def append(self, value: str) -> None:
        """Append a button label so expression construction remains centralized."""
        self.expression += value

    def clear(self) -> None:
        """Clear all entered text when the user presses the C button."""
        self.expression = ""

    def evaluate(self) -> None:
        """Replace the expression with its result or Error without raising to the UI."""
        try:
            tree = ast.parse(self.expression, mode="eval")
            self.expression = str(self._evaluate_node(tree.body))
        except (ArithmeticError, SyntaxError, TypeError, ValueError):
            self.expression = "Error"

    def _evaluate_node(self, node: ast.AST) -> Number:
        """Recursively calculate a whitelisted arithmetic tree and reject everything else."""
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            operation = OPERATORS[type(node.op)]
            return operation(self._evaluate_node(node.left), self._evaluate_node(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](self._evaluate_node(node.operand))
        raise ValueError("Unsupported expression")