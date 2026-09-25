import ast
from typing import Tuple, List

BANNED_CALLS = {
    "system", "popen", "spawn", "exec", "eval", "__import__", "rmtree"
}

BANNED_MODULES = {
    "pty", "shutil"
}

class SecurityASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.violations: List[str] = []
        self.node_count: int = 0

    def visit(self, node):
        self.node_count += 1
        return super().visit(node)

    def visit_Call(self, node: ast.Call):
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name and func_name.lower() in BANNED_CALLS:
            self.violations.append(f"Prohibited call detected in hotpatch: '{func_name}()'")

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name.lower() in BANNED_MODULES:
                self.violations.append(f"Prohibited module import in hotpatch: '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module and node.module.lower() in BANNED_MODULES:
            self.violations.append(f"Prohibited module import in hotpatch: '{node.module}'")
        self.generic_visit(node)

def validate_python_code(source_code: str) -> Tuple[bool, int, str]:
    """
    Validates that a piece of Python code parses into a valid Abstract Syntax Tree (AST)
    and passes security linting (no hazardous system execution).
    
    Returns:
        (is_valid: bool, node_count: int, message: str)
    """
    if not source_code or not source_code.strip():
        return False, 0, "Source code cannot be empty"

    try:
        parsed_tree = ast.parse(source_code)
    except SyntaxError as e:
        return False, 0, f"AST SyntaxError on line {e.lineno}, col {e.offset}: {e.msg}"
    except Exception as e:
        return False, 0, f"AST Parse failure: {str(e)}"

    visitor = SecurityASTVisitor()
    visitor.visit(parsed_tree)

    if visitor.violations:
        return False, visitor.node_count, f"Security policy rejection: {'; '.join(visitor.violations)}"

    return True, visitor.node_count, "AST validation passed successfully. Clean and valid Python syntax."
