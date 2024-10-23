from flask import Flask, request, jsonify, send_from_directory
from .ast_engine import build_ast, combine_rules, evaluate_ast

app = Flask(__name__, static_folder='../static', static_url_path='')

rules = {}

@app.route('/')
def index():
    return send_from_directory('../static', 'index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule')
    rule_ast = build_ast(rule_string)
    rule_id = len(rules) + 1
    rules[rule_id] = rule_ast
    return jsonify({"rule_id": rule_id, "ast": str(rule_ast)})

@app.route('/combine_rules', methods=['POST'])
def combine_rule():
    rule_ids = request.json.get('rule_ids')
    rule_asts = [rules[rule_id] for rule_id in rule_ids]
    combined_ast = combine_rules(rule_asts)
    return jsonify({"combined_ast": str(combined_ast)})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    rule_id = request.json.get('rule_id')
    user_data = request.json.get('data')
    result = evaluate_ast(rules[rule_id], user_data)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
