import os
VERBOSE = os.getenv("PT_VERBOSE", "1") == "1"

def log(msg):
    if VERBOSE:
        print(msg, flush=True)