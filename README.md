# PET Literature Miner

A modular Python tool for mining and analyzing scientific literature related to **PET tracers** and **oncology**.

It reads paper data, cleans the text, tags papers with relevant keywords, and stores results in a local SQLite database for easy querying.

---

## Project Structure

```
pet_literature_miner/
│
├── src/
│   ├── parser.py     # Load and parse paper data from files
│   ├── cleaner.py    # Clean and normalize text
│   ├── tagger.py     # Tag papers with PET tracer and oncology keywords
│   ├── database.py   # Save and retrieve papers using SQLite
│   └── main.py       # Main pipeline — run this to process papers
│
├── data/             # Put your raw paper JSON files here; database is saved here too
├── tests/            # Unit tests for each module
├── notebooks/        # Jupyter notebooks for exploration and visualization
│
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Getting Started

### 1. Clone or download the project

```bash
git clone <your-repo-url>
cd pet_literature_miner
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add paper data

Place your paper files inside the `data/` folder. The tool supports both **JSON and PDF formats**.

For JSON files, use this structure:

```json
{
  "title": "FDG-PET in staging of non-small cell lung cancer",
  "abstract": "Background: FDG-PET has been shown to improve staging accuracy...",
  "authors": ["Smith J", "Doe A"],
  "year": 2023,
  "doi": "10.1000/example.doi"
}
```

### 5. Run the pipeline

```bash
python src/main.py
```

This will:
1. Load all JSON and PDF files from `data/`
2. Clean the text in each paper
3. Tag papers with PET tracer and oncology keywords
4. Save results to `data/papers.db` (SQLite)
5. Print a summary to the terminal

---

## Module Overview

| File | Purpose |
|------|---------|
| `parser.py` | Reads JSON and PDF paper files and returns structured dicts |
| `cleaner.py` | Removes noise from text (whitespace, special chars) |
| `tagger.py` | Matches keywords for PET tracers and oncology topics |
| `database.py` | Creates the SQLite DB, inserts and queries papers |
| `main.py` | Orchestrates the full pipeline end-to-end |

---

## PET Tracer Keywords (examples)

`FDG`, `18F-FDG`, `PSMA`, `DOTATATE`, `DOTATOC`, `FLT`, `FMISO`, `Ga-68`, `Zr-89`, and more.

You can extend the keyword lists in `tagger.py` to match your research needs.

---

## Running Tests

```bash
pytest tests/
```

---

## Requirements

- Python 3.9+
- See `requirements.txt` for full dependency list
