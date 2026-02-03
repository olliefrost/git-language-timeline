import subprocess
import matplotlib.pyplot as plt
from collections import Counter
import os

# File extension → language mapping
EXTENSIONS = {
    # C / C++
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".hpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",

    # C#
    ".cs": "C#",

    # CSS
    ".css": "CSS",

    # Go
    ".go": "Go",

    # Haskell
    ".hs": "Haskell",

    # HTML
    ".html": "HTML",
    ".htm": "HTML",

    # Java / Kotlin
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",

    # JavaScript / TypeScript
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",

    # Lua
    ".lua": "Lua",

    # PHP
    ".php": "PHP",

    # Python
    ".py": "Python",

    # Ruby
    ".rb": "Ruby",

    # Rust
    ".rs": "Rust",

    # Scala
    ".scala": "Scala",

    # Shell
    ".sh": "Shell",

    # Swift
    ".swift": "Swift",

    # Verilog
    ".v": "Verilog",
}

# Paths to ignore (e.g. "vendor/", "tests/file.py")
# These are checked against the relative path from the repo root.
IGNORED_PATHS = [
    # "vendor/lib/",
]

LANGUAGES = sorted(list(set(EXTENSIONS.values())))

import argparse
from datetime import datetime

# Parse arguments
parser = argparse.ArgumentParser(description="Visualise language usage over time (File Count).")
parser.add_argument(
    "--mode",
    choices=["commits", "time"],
    default="commits",
    help="X-axis mode: 'commits' (default) or 'time'",
)
args = parser.parse_args()

# Get commits from oldest to newest with timestamps
raw_commits = subprocess.check_output(
    ["git", "log", "--reverse", "--format=%H %at", "HEAD"]
).decode().splitlines()

commits = []
timestamps = []

for line in raw_commits:
    parts = line.split()
    if len(parts) >= 2:
        commits.append(parts[0])
        timestamps.append(int(parts[1]))

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
            path = os.path.join(root, f)
            # Remove ./ prefix for cleaner matching if present
            rel_path = os.path.normpath(path)
            
            # Check ignored paths
            if any(rel_path.startswith(os.path.normpath(i)) for i in IGNORED_PATHS):
                continue
                
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

# Prepare X-axis data
if args.mode == "time":
    x_values = [datetime.fromtimestamp(ts) for ts in timestamps]
    plt.xlabel("Date")
    plt.gcf().autofmt_xdate()
else:
    num_points = len(next(iter(history.values()))) if history else 0
    x_values = range(num_points)
    plt.xlabel("Commits")

for lang, values in history.items():
    if max(values) > 0:
        plt.plot(x_values, values, label=lang)

plt.title("Language Usage Over Time")
plt.ylabel("Percentage of Files")
plt.legend()
plt.tight_layout()
plt.show()

