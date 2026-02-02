import os
import sys
import shutil
import importlib.util

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load module dynamically because of hyphen in name
spec = importlib.util.spec_from_file_location("impl", os.path.join(os.path.dirname(__file__), '../skills/file-system/impl.py'))
impl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(impl)

def test_office_skill():
    workspace_dir = os.path.abspath("test_workspace")
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir)
    os.makedirs(workspace_dir)
    
    print(f"Testing in {workspace_dir}")
    
    # 1. DOCX
    print("Testing DOCX...")
    res = impl.write_docx(workspace_dir, "test.docx", "Hello World\nThis is a test.")
    print(f"Write DOCX: {res}")
    # Unified read
    content = impl.read_file(workspace_dir, "test.docx")
    print(f"Read DOCX (via read_file): {content}")
    assert "Hello World" in content
    
    # 2. PPTX
    print("\nTesting PPTX...")
    slides = [{"title": "Title 1", "content": "Content 1"}, {"title": "Title 2", "content": "Content 2"}]
    res = impl.create_pptx(workspace_dir, "test.pptx", slides)
    print(f"Create PPTX: {res}")
    # Unified read
    content = impl.read_file(workspace_dir, "test.pptx")
    print(f"Read PPTX (via read_file): {content}")
    assert "Title 1" in content
    
    # 3. Excel
    print("\nTesting Excel...")
    data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]
    res = impl.write_excel(workspace_dir, "test.xlsx", data)
    print(f"Write Excel: {res}")
    # Unified read
    content = impl.read_file(workspace_dir, "test.xlsx")
    print(f"Read Excel (via read_file): \n{content}")
    assert "Alice" in content

    # 4. Plain Text
    print("\nTesting Plain Text...")
    txt_path = os.path.join(workspace_dir, "test.txt")
    with open(txt_path, 'w') as f:
        f.write("Just some text")
    content = impl.read_file(workspace_dir, "test.txt")
    print(f"Read Text (via read_file): {content}")
    assert "Just some text" in content
    
    # Cleanup
    # shutil.rmtree(workspace_dir)
    print("\nTest Complete.")

if __name__ == "__main__":
    test_office_skill()
