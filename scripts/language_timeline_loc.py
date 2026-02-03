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

def count_non_empty_lines(path):
    """Count non-empty lines in a text file."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for line in f if line.strip())
    except OSError:
        return 0

# Get commits oldest → newest
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
    total_lines = 0

    for root, _, files in os.walk("."):
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
                lines = count_non_empty_lines(path)
                lang = EXTENSIONS[ext]

                counter[lang] += lines
                total_lines += lines

    for lang in LANGUAGES:
        history[lang].append(
            counter[lang] / total_lines * 100 if total_lines else 0
        )

# Restore branch
subprocess.run(["git", "checkout", "--quiet", "main"])

# Plot
plt.figure(figsize=(12, 6))

for lang, values in history.items():
    if max(values) > 0:
        plt.plot(values, label=lang)

plt.title("Language Usage Over Time (Lines of Code)")
plt.xlabel("Commits")
plt.ylabel("Percentage of LOC")
plt.legend()
plt.tight_layout()
plt.show()
