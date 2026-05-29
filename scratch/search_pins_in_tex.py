import os
import re

for filename in os.listdir('.'):
    if filename.endswith('.tex'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # find all occurrences of dht11, ldr, rele, sonido, gpio, pin, D26, D27, D32, etc.
            matches = re.findall(r'.{0,50}(?:dht11|ldr|rele|relé|sonido|gpio|D26|D27|D32|D4).{0,50}', content, re.IGNORECASE)
            if matches:
                print(f"--- {filename} ---")
                for match in matches[:20]:
                    print(match.strip())
