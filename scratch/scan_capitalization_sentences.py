import os
import re

tex_files = ['1_introduccion.tex', '2_contexto_estado_arte.tex', '3_analisis_requisitos.tex', 
             '4_diseno_sistema.tex', '5_seleccion_tecnologias.tex', '6_plan_implantacion.tex', 
             '7_evaluacion_sistema.tex', '8_presupuesto.tex', '9_planos_esquemas.tex', '10_conclusiones.tex']

allowed_acronyms = {
    'ESP32', 'SoC', 'Docker', 'Portainer', 'Home', 'Assistant', 'SQLite', 'Tailscale', 'WireGuard',
    'Wi-Fi', 'Ethernet', 'UART', 'GPIO', 'CPU', 'RAM', 'LDR', 'DHT11', 'FMCW', 'ISM', 'Noise',
    'YAML', 'TCP', 'IP', 'VPN', 'HTTP', 'HTTPS', 'IEEE', 'Lovelace', 'Sonoff', 'Tuya', 'Smart',
    'eWeLink', 'SmartLife', 'JSON', 'XML', 'PC', 'OS', 'LED', 'ADC', 'DAC', 'GND', 'VIN', 'TX',
    'RX', 'TX2', 'RX2', 'TTL', 'HTML', 'CSS', 'WAN', 'WLAN', 'DNS', 'UCO', 'TFG', 'FSM', 'PIR',
    'SSD', 'NAS', 'TinyML', 'TensorFlow', 'Lite', 'Whisper', 'Piper', 'Babel', 'TikZ', 'LaTeX', 'TeX', 'PDF'
}

def clean_latex_macros(text):
    # Remove commands like \texttt{...}, \lstinline{...}, \ref{...}, \cite{...}, \label{...}
    # But keep their contents if they are running text (e.g. \textbf{Word} -> Word)
    # Let's do a simple replacement for common macros that contain non-text
    text = re.sub(r'\\label\{[^}]+\}', '', text)
    text = re.sub(r'\\ref\{[^}]+\}', '', text)
    text = re.sub(r'\\cite\{[^}]+\}', '', text)
    text = re.sub(r'\\url\{[^}]+\}', '', text)
    text = re.sub(r'\\texttt\{[^}]+\}', '', text) # texttt often contains code symbols
    text = re.sub(r'\\lstinline\s*[^a-zA-Z\s]', '', text) # simple lstinline strip
    return text

for file_name in tex_files:
    print(f"\n=== Capitalization in {file_name} ===")
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split content into paragraphs (split by double newline)
    paragraphs = content.split('\n\n')
    for p_num, p in enumerate(paragraphs, 1):
        p_clean = p.strip()
        if not p_clean or p_clean.startswith('%') or '\\begin{' in p_clean or '\\end{' in p_clean:
            continue
            
        p_text = clean_latex_macros(p_clean)
        
        # Split paragraph into sentences by simple punctuation (. ! ?) followed by space or newline
        sentences = re.split(r'(?<=[.!?])\s+', p_text)
        for s in sentences:
            s = s.strip()
            if not s:
                continue
                
            # Find words that are capitalized
            # We want to ignore the first word of the sentence
            # First, clean up leading LaTeX commands at the start of sentence, e.g. \textbf{En primer lugar} -> En primer lugar
            s_clean = re.sub(r'^\\[a-zA-Z]+\s*\{', '', s)
            # Find all words
            words = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-zA-Záéíóúñ]+\b', s_clean)
            if not words:
                continue
                
            # The first word in s_clean is usually capitalized because it's the start of the sentence
            # Let's find what the first word is
            first_word_match = re.search(r'\b[a-zA-Záéíóúñ]+\b', s_clean)
            first_word = first_word_match.group(0) if first_word_match else ""
            
            for word in words:
                if word == first_word:
                    continue # First word of sentence is allowed to be capitalized
                if word in allowed_acronyms:
                    continue
                if word.isupper():
                    continue # Acronyms like FSM, RPI, etc.
                    
                # Get index of word to print context
                idx = s_clean.find(word)
                context = s_clean[max(0, idx-40):min(len(s_clean), idx+40)].replace('\n', ' ')
                print(f"  Sentence: \"{s[:80]}...\"")
                print(f"    Word: '{word}' in context: ...{context}...")
                print("-" * 40)
