# Language Usage Timeline

This tool generates a time-series graph showing how the composition of a Git
repository changes over time, measured as the **percentage of files per
programming language** at each commit.

Each language is plotted as a line, allowing you to see when languages are
introduced, grow, or decline throughout the project’s history.

---

## What This Shows

- One line per language
- X-axis: commits (from first commit to latest)
- Y-axis: percentage of files in the repository
- Languages are grouped by file extension:
  - C (`.c`, `.h`)
  - Haskell (`.hs`)
  - Python (`.py`)
  - Java (`.java`)
  - Verilog (`.v`, `.vcd`, `.vvp`)

This focuses on **file counts**, not lines of code.

---

## Requirements

- Python 3.9+
- Git
- Python packages:
  - `matplotlib`

Install dependencies in a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install matplotlib
