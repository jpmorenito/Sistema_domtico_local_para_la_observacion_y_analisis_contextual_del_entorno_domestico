with open('10_conclusiones.tex', 'rb') as f:
    raw = f.read()

print("Raw length:", len(raw))
# Let's check some bytes around "señales:"
# "señales:" in UTF-8: s (115) e (101) ñ (195 177) a (97) l (108) e (101) s (115) : (58)
# "señales:" in ISO-8859-1: s (115) e (101) ñ (241) a (97) l (108) e (101) s (115) : (58)

idx = raw.find(b':')
while idx != -1:
    print(f"Colon at {idx}:")
    start = max(0, idx - 10)
    end = min(len(raw), idx + 10)
    print("  Bytes:", raw[start:end])
    # Try decoding
    try:
        print("  Decoded (utf-8):", raw[start:end].decode('utf-8'))
    except Exception as e:
        print("  utf-8 error:", e)
    try:
        print("  Decoded (iso-8859-1):", raw[start:end].decode('iso-8859-1'))
    except Exception as e:
        print("  iso error:", e)
    idx = raw.find(b':', idx + 1)
