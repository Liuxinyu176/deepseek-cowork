import sys
import os
import shutil

def get_python_executable():
    """
    Get the path to the Python executable to use for subprocesses.
    Prioritizes the bundled 'python_env' in frozen mode to ensure consistency.
    """
    # 1. If not frozen (Dev Mode), use the current interpreter
    if not getattr(sys, 'frozen', False):
        return sys.executable

    # 2. Frozen Mode: Search for bundled python
    # We expect a 'python_env' folder to be bundled with the application.
    # Locations to check:
    # - sys._MEIPASS/python_env/python.exe (OneFile temp dir)
    # - base_dir/python_env/python.exe (OneDir next to exe)
    # - base_dir/_internal/python_env/python.exe (PyInstaller internal)
    
    base_dir = os.path.dirname(sys.executable)
    possible_paths = [
        os.path.join(base_dir, "python_env", "python.exe"),
        os.path.join(base_dir, "_internal", "python_env", "python.exe")
    ]
    
    if hasattr(sys, '_MEIPASS'):
        possible_paths.insert(0, os.path.join(sys._MEIPASS, "python_env", "python.exe"))
        
    for p in possible_paths:
        if os.path.exists(p):
            return p
            
    # 3. Fallback: If no bundled python found
    # We return 'python' to try the system PATH, but this implies the packaging was incomplete.
    return "python"
