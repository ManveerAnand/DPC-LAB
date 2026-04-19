import sys
import subprocess

try:
    import pypdf
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    import pypdf

reader = pypdf.PdfReader(r"D:\Dev 2.0\DPC\LAB 7\Lab_7_Qustions.pdf")
text = "\n".join(p.extract_text() for p in reader.pages)
with open(r"D:\Dev 2.0\DPC\LAB 7\pdf_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("PDF extracted successfully!")
