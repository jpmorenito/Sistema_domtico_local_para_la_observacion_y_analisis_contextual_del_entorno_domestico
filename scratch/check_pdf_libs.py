import sys

packages = ["fitz", "pdf2image", "pypdf", "pdfplumber", "reportlab"]
for package in packages:
    try:
        __import__(package)
        print(f"Paquete {package} está disponible")
    except ImportError:
        print(f"Paquete {package} NO está disponible")
