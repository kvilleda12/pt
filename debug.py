import os
import sys

print("--- Diagnostic Info ---")

# 1. Current Working Directory
cwd = os.getcwd()
print(f"Current Directory (pwd): {cwd}")

# 2. Python Executable
print(f"Python Executable: {sys.executable}")

# 3. Python Search Path (sys.path)
print("\nPython Search Path (sys.path):")
for p in sys.path:
    print(f"- {p}")

# 4. Check for critical __init__.py files
print("\nChecking for __init__.py files:")
backend_init = os.path.exists('backend/__init__.py')
pipeline_init = os.path.exists('backend/pipeline/__init__.py')
print(f"backend/__init__.py exists: {backend_init}")
print(f"backend/pipeline/__init__.py exists: {pipeline_init}")

# 5. Check if the run_pipeline.py file exists
print("\nChecking for run_pipeline.py file:")
run_script_exists = os.path.exists('backend/pipeline/run_pipeline')
print(f"backend/pipeline/run_pipeline.py exists: {run_script_exists}")

print("\n--- End Diagnostic Info ---")