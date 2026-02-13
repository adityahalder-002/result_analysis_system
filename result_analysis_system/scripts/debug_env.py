import sys
import site
import os

print(f"Executable: {sys.executable}")
print(f"CWD: {os.getcwd()}")
print("Sys Path:")
for p in sys.path:
    print(p)

print("\nSite Packages:")
for p in site.getsitepackages():
    print(p)

try:
    import pdfplumber
    print("\npdfplumber imported successfully")
    print(f"File: {pdfplumber.__file__}")
except ImportError as e:
    print(f"\nFailed to import pdfplumber: {e}")
