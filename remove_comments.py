import os
import re

def remove_comments(content):
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            cleaned_lines.append('')
            continue
        
        # Find comment position (# not in string)
        in_string = False
        string_char = None
        comment_pos = -1
        
        i = 0
        while i < len(line):
            char = line[i]
            
            # Handle string literals
            if char in ('"', "'") and (i == 0 or line[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
            
            # Find comment outside of string
            if char == '#' and not in_string:
                comment_pos = i
                break
            
            i += 1
        
        if comment_pos >= 0:
            # Line has a comment
            code_part = line[:comment_pos].rstrip()
            if code_part:  # Only keep if there's code before the comment
                cleaned_lines.append(code_part)
            elif not code_part:  # Comment-only line
                cleaned_lines.append('')
        else:
            # No comment
            cleaned_lines.append(line)
    
    # Remove trailing empty lines and rejoin
    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()
    
    return '\n'.join(cleaned_lines)

# Process all Python files
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['env', '__pycache__', '.pytest_cache', 'reports', '.git']]
    
    for file in files:
        if file.endswith('.py') and file != 'remove_comments.py':
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                modified = remove_comments(content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(modified)
                
                print(f"✓ {filepath}")
            except Exception as e:
                print(f"✗ {filepath}: {e}")

print("\nDone! All comments removed.")
