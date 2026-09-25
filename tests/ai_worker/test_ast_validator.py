import pytest
import sys
from pathlib import Path

# Add apps/ai-worker to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "ai-worker"))

from app.services.ast_validator import validate_python_code

def test_ast_valid_python():
    valid_code = """
def calculate_discount(price: float, discount: float) -> float:
    if discount <= 0:
        return price
    return price * (1 - discount)
"""
    is_valid, nodes, msg = validate_python_code(valid_code)
    assert is_valid is True
    assert nodes > 0
    assert "AST validation passed" in msg

def test_ast_invalid_syntax():
    broken_code = """
def broken_function(:
    return 42
"""
    is_valid, nodes, msg = validate_python_code(broken_code)
    assert is_valid is False
    assert "SyntaxError" in msg

def test_ast_security_rejection_os_system():
    malicious_code = """
import os
def exploit():
    os.system("rm -rf /")
"""
    is_valid, nodes, msg = validate_python_code(malicious_code)
    assert is_valid is False
    assert "Prohibited call" in msg

def test_ast_security_rejection_eval():
    unsafe_code = """
def unsafe_eval(user_input):
    return eval(user_input)
"""
    is_valid, nodes, msg = validate_python_code(unsafe_code)
    assert is_valid is False
    assert "Prohibited call" in msg
