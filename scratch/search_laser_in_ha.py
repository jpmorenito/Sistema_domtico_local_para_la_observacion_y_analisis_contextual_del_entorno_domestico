with open("c:/Users/jacob/Downloads/TFG/pi_automations.yaml", "r", encoding="utf-8") as f:
    content = f.read()

if "laser_escritorio" in content:
    print("Found 'laser_escritorio' in pi_automations.yaml")
    # Print lines around it
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "laser_escritorio" in line:
            print(f"Line {i+1}: {line}")
else:
    print("'laser_escritorio' NOT found in pi_automations.yaml")
