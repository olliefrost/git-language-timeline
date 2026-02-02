import subprocess
import matplotlib.pyplot as plt
from collections import Counter
import os

# File extension → language mapping
EXTENSIONS = {
    ".c": "C",
    ".h": "C",

    ".hs": "Haskell",

    ".py": "Python",

    ".java": "Java",

    # Verilog and related files
    ".v": "Verilog",
    ".vcd": "Verilog",
    ".vvp": "Verilog",
}

LANGUAGES = ["C", "Haskell", "Python", "Java", "Verilog"]

# Get commits from oldest to newest
commits = subprocess.check_output(
    ["git", "rev-list", "--reverse", "HEAD"]
).decode().splitlines()

history = {lang: [] for lang in LANGUAGES}

for commit in commits:
    subprocess.run(
        ["git", "checkout", "--quiet", commit],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    counter = Counter()
    total = 0

    for root, _, files in os.walk("."):
        # Ignore Git internals
        if root.startswith("./.git"):
            continue

        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in EXTENSIONS:
                lang = EXTENSIONS[ext]
                counter[lang] += 1
                total += 1

    for lang in LANGUAGES:
        history[lang].append(counter[lang] / total * 100 if total else 0)

# Restore original branch
subprocess.run(["git", "checkout", "--quiet", "main"])

# Plot results
plt.figure(figsize=(12, 6))

for lang, values in history.items():
    if max(values) > 0:
        plt.plot(values, label=lang)

plt.title("Language Usage Over Time")
plt.xlabel("Commits")
plt.ylabel("Percentage of Files")
plt.legend()
plt.tight_layout()
plt.show()

