import sys
import subprocess
import tempfile
import os
import ast
import shutil

class SecurityError(Exception):
    pass

def validate_code_safety(code, allowed_dir):
    """AST static analysis for code safety"""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise SecurityError(f"Syntax Error: {e}")

    allowed_dir = os.path.abspath(allowed_dir).lower()

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            val = node.value
            if ".." in val:
                 raise SecurityError(f"Security Alert: Path traversal '..' detected in string: '{val}'")
            if os.path.isabs(val):
                abs_val = os.path.abspath(val).lower()
                if not abs_val.startswith(allowed_dir):
                     raise SecurityError(f"Security Alert: Unauthorized absolute path access: '{val}'")
    return True

def run_python_code(workspace_dir, code):
    """
    Execute Python code in the workspace.
    
    Args:
        workspace_dir (str): Root workspace directory.
        code (str): Python code to execute.
    """
    if not workspace_dir:
        return "Error: Workspace not selected."
        
    try:
        validate_code_safety(code, workspace_dir)
    except SecurityError as e:
        return f"Error: {str(e)}"

    # Create temp file
    temp_path = ""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_path = f.name
    except Exception as e:
        return f"Error creating temp file: {e}"

    # Determine python executable
    python_exe = sys.executable
    if getattr(sys, 'frozen', False):
         # In frozen mode, try to find system python
         sys_python = shutil.which("python")
         if sys_python:
             python_exe = sys_python
         else:
             return "Error: System 'python' not found in PATH. Cannot execute scripts in frozen mode."
    
    try:
        # Run subprocess
        result = subprocess.run(
            [python_exe, temp_path],
            capture_output=True,
            text=True,
            cwd=workspace_dir,
            encoding='utf-8',
            errors='replace',
            timeout=30 # 30s timeout
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nStderr: {result.stderr}"
            
        return output if output.strip() else "(No output)"
        
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out (30s)."
    except Exception as e:
        return f"Error executing code: {str(e)}"
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
