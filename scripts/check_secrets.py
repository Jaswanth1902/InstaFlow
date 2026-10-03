import os
import re

patterns = [
    re.compile(r'(?i)api[_-]?key\s*[:=]\s*["\'][a-zA-Z0-9_\-]{20,}'),
    re.compile(r'ghp_[a-zA-Z0-9]{36}'),
    re.compile(r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ')
]

found = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', '__pycache__', 'node_modules', '_frames']):
        continue
    for f in files:
        if f.endswith(('.py', '.html', '.md', '.json', '.txt', '.toml')):
            p = os.path.join(root, f)
            try:
                content = open(p, 'r', encoding='utf-8', errors='ignore').read()
                for pat in patterns:
                    if pat.search(content):
                        found.append(p)
                        break
            except Exception:
                pass

if found:
    print('VULNERABILITIES FOUND:', found)
else:
    print('CLEAN: Zero secrets found in any text files.')
