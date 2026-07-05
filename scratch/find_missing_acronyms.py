import os
import re

# List of defined abbreviations in __memoria.tex
defined_abbreviations = {
    'API', 'DHT', 'ESP', 'GPIO', 'HA', 'I2C', 'IDE', 'IoT', 'LDR', 
    'MAC', 'MQTT', 'OS', 'OTA', 'PIR', 'PWM', 'RAM', 'SBC', 'SSR', 
    'UI', 'VPN', 'YAML'
}

# Find all .tex files
tex_files = [f for f in os.listdir('.') if f.endswith('.tex')]

# Regular expression to find uppercase acronyms (2 to 7 letters)
acronym_pattern = re.compile(r'\b[A-Z]{2,7}\b')

found_acronyms = set()

# Words to ignore (common Spanish short uppercase words, document parts, and some standard formatting)
ignore_words = {
    'UCO', 'TFG', 'II', 'III', 'IV', 'VI', 'VII', 'VIII', 'IX', 'X', 
    'AND', 'OR', 'GND', 'VIN', 'VCC', 'TX', 'RX', 'RX2', 'TX2', 'GATT', 'GAP',
    'ON', 'OFF', 'NO', 'SI', 'OK', 'URL', 'DOI', 'PDF', 'SAI', 'CPU', 'RAM', 'ROM',
    'USB', 'ASCII', 'ISO', 'IEC', 'IEEE', 'FSM', 'BLE', 'WAN', 'WLAN', 'LPWAN',
    'mDNS', 'UPnP', 'NAT', 'DNS', 'FMCW', 'ADC', 'UART', 'AmI', 'FSM', 'noise', 'NOISE',
    'LDR', 'PIR', 'DHT', 'API', 'GPIO', 'MQTT', 'VPN', 'YAML', 'SBC', 'SSR', 'UI', 'HA'
}

# Read through all files
for filename in tex_files:
    # Skip temporary files or backup files
    if filename.startswith('ALMCACENAMIENTO') or filename.startswith('bak'):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        comment_start = -1
        for idx, char in enumerate(line):
            if char == '%':
                if idx == 0 or line[idx-1] != '\\':
                    comment_start = idx
                    break
        if comment_start != -1:
            line = line[:comment_start]
        cleaned_lines.append(line)
    
    content_clean = ' '.join(cleaned_lines)
    
    # Find all matches
    matches = acronym_pattern.findall(content_clean)
    for match in matches:
        found_acronyms.add(match)

# Filter out defined ones and ignored ones
missing_candidates = found_acronyms - defined_abbreviations - ignore_words

print("Found acronyms in text:")
print(sorted(list(found_acronyms)))

print("\nMissing candidates from abbreviation list (unfiltered):")
print(sorted(list(missing_candidates)))
