import os
import sys
import subprocess

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
os.chdir(backend_dir)

result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_auth.py", "-v"], capture_output=True, text=True)

with open("test_output.txt", "w", encoding="utf-8") as f:
    f.write(result.stdout)
    f.write("\n")
    f.write(result.stderr)
