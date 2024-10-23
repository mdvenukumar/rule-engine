import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        """
        node_type: "operator" (AND/OR) or "operand" (conditions)
        left: Left child Node (for operators)
        right: Right child Node (for operators)
        value: Condition string or operator (for operands)
        """
        self.type = node_type  # 'operator' or 'operand'
        self.left = left       # Left child for operators
        self.right = right     # Right child for operators
        self.value = value     # For operands, condition like 'age > 30'

    def __repr__(self):
        return f"Node(type={self.type}, left={self.left}, right={self.right}, value={self.value})"

def parse_condition(condition):
    """Parse a condition (e.g., 'age > 30') into a Node."""
    return Node("operand", value=condition)

def parse_operator(operator):
    """Parse an operator ('AND', 'OR') into a Node."""
    return Node("operator", value=operator)

def build_ast(rule_string):
    """
    Build an AST from a rule string like:
    ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))
    """
    tokens = re.split(r'(\(|\)|AND|OR)', rule_string)
    tokens = [token.strip() for token in tokens if token.strip()]
    stack = []

    for token in tokens:
        if token == "(":
            stack.append(token)
        elif token == ")":
            right = stack.pop()
            operator = stack.pop()
            left = stack.pop()
            stack.pop()  # Remove '('
            node = Node("operator", left=left, right=right, value=operator.value)
            stack.append(node)
        elif token in ["AND", "OR"]:
            stack.append(parse_operator(token))
        else:
            stack.append(parse_condition(token))

    return stack[0] if stack else None

def combine_rules(rules):
    """Combine multiple rules into a single AST."""
    combined_ast = None
    for rule_string in rules:
        rule_ast = build_ast(rule_string)
        if combined_ast:
            combined_ast = Node("operator", left=combined_ast, right=rule_ast, value="AND")
        else:
            combined_ast = rule_ast
    return combined_ast

def evaluate_ast(ast, data):
    """Evaluate the AST using provided user data."""
    if ast.type == "operand":
        # Assuming simple conditions like 'age > 30'
        condition = ast.value
        key, operator, value = re.split(r'(\>|\<|=)', condition)
        key = key.strip()
        value = int(value.strip()) if value.strip().isdigit() else value.strip().replace("'", "")
        data_value = data.get(key)

        if operator == ">":
            return data_value > value
        elif operator == "<":
            return data_value < value
        elif operator == "=":
            return data_value == value
    elif ast.type == "operator":
        if ast.value == "AND":
            return evaluate_ast(ast.left, data) and evaluate_ast(ast.right, data)
        elif ast.value == "OR":
            return evaluate_ast(ast.left, data) or evaluate_ast(ast.right, data)
    return False
