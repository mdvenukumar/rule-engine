import unittest
from app.ast_engine import build_ast, evaluate_ast

class TestRuleEngine(unittest.TestCase):

    def test_simple_rule(self):
        rule = "(age > 30 AND salary > 50000)"
        ast = build_ast(rule)
        data = {'age': 35, 'salary': 60000}
        self.assertTrue(evaluate_ast(ast, data))

        data = {'age': 25, 'salary': 40000}
        self.assertFalse(evaluate_ast(ast, data))

if __name__ == '__main__':
    unittest.main()
