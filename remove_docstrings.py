import os
import re

def remove_docstrings(content):
    """Remove docstrings from Python code"""
    # Remove standalone docstrings
    content = re.sub(r'^\s*""".*?"""\s*\n', '', content, flags=re.MULTILINE | re.DOTALL)
    content = re.sub(r"^\s*'''.*?'''\s*\n", '', content, flags=re.MULTILINE | re.DOTALL)
    return content

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['env', '__pycache__', '.pytest_cache', 'reports']]
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                modified = remove_docstrings(content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(modified)
                
                print(f"✓ {filepath}")
            except Exception as e:
                print(f"✗ {filepath}: {e}")

print("\nAll docstrings removed!")
