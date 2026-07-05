import re

def check_environments(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments
    content = re.sub(r'%.*?\n', '\n', content)
    
    begins = re.findall(r'\\begin\{([a-zA-Z*]+)\}', content)
    ends = re.findall(r'\\end\{([a-zA-Z*]+)\}', content)
    
    print(f"File: {filepath}")
    print(f"Begins: {begins}")
    print(f"Ends: {ends}")
    
    # Track nesting
    stack = []
    for match in re.finditer(r'\\(begin|end)\{([a-zA-Z*]+)\}', content):
        cmd, env = match.groups()
        if cmd == 'begin':
            stack.append((env, match.start()))
        else:
            if not stack:
                print(f"Extra \\end{{{env}}} at char {match.start()}")
            else:
                top_env, pos = stack.pop()
                if top_env != env:
                    print(f"Mismatched environments: \\begin{{{top_env}}} at {pos} vs \\end{{{env}}} at {match.start()}")
    
    if stack:
        print(f"Unclosed environments at end of {filepath}:")
        for env, pos in stack:
            # print surrounding text
            surr = content[max(0, pos-20):min(len(content), pos+50)].replace('\n', ' ')
            print(f"  \\begin{{{env}}} at char {pos}: ... {surr} ...")

check_environments(r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.tex")
