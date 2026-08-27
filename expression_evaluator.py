"""Build and safely evaluate the calculator expression."""

import ast
import operator
from collections.abc import Callable
from typing import Final


Number = int | float
Operation = Callable[..., Number]

ALLOWED_OPERATIONS: Final[dict[type[ast.operator], Operation]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_expression(expression: str) -> str:
    """Return an arithmetic result, or ``Error`` for invalid input."""
    try:
        tree = ast.parse(expression, mode="eval")
        return str(evaluate_node(tree.body))
    except (ArithmeticError, SyntaxError, TypeError, ValueError):
        return "Error"


def evaluate_node(node: ast.AST) -> Number:
    """Evaluate one approved AST node recursively."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATIONS:
        operation = ALLOWED_OPERATIONS[type(node.op)]
        return operation(evaluate_node(node.left), evaluate_node(node.right))

    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATIONS:
        return ALLOWED_OPERATIONS[type(node.op)](evaluate_node(node.operand))

    raise ValueError("Unsupported expression")