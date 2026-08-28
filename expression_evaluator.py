"""Evaluate the calculator expression."""


def evaluate_expression(expression: str) -> str:
    """Return an arithmetic result, or ``Error`` for invalid input."""
    allowed_characters = "0123456789+-*/(). "

    if not expression or any(character not in allowed_characters for character in expression):
        return "Error"
    if "**" in expression or "//" in expression:
        return "Error"

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        if not isinstance(result, (int, float)):
            return "Error"
        return str(result)
    except (ArithmeticError, SyntaxError, TypeError, ValueError):
        return "Error"