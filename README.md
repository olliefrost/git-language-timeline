# Git Language Timeline

Visualise how programming language usage changes over time in a Git repository.

This project provides two scripts that analyse a repository’s commit history and plot language usage as a percentage over time.

---

## Repository Structure

```

git-language-timeline/
├── scripts/
│   ├── language_timeline_files.py   # file-count based metric
│   └── language_timeline_loc.py     # line-of-code based metric
├── requirements.txt
└── README.md

````

---

## Metrics

Two different metrics are supported.

### File Count

Measures language usage by the number of tracked files.

- Each file counts equally
- Fast to compute
- Good for structural trends

Run:
```bash
python scripts/language_timeline_files.py
````

---

### Lines of Code (LOC)

Measures language usage by counting non-empty lines of code.

* More representative of code volume
* Slower to compute
* Comment lines are included

Run:

```bash
python scripts/language_timeline_loc.py
```

---

## Installation

It is recommended to use a virtual environment.

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

---

## Usage

Run the scripts from the **root of the repository you want to analyse**:

```bash
python scripts/language_timeline_files.py
# or
python scripts/language_timeline_loc.py
```

A matplotlib graph will open showing language usage across the full commit history.

---

## Notes

* The repository must be a Git repository
* Binary and unreadable files are ignored
* All tracked files are included
* The working tree is restored after execution

---

## License

MIT


