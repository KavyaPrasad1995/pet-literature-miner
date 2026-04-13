# parser.py
# This module is responsible for reading and parsing scientific papers.
# It handles loading paper data from files (e.g., XML, JSON, plain text)
# and extracting key fields like title, abstract, authors, and publication date.
# Think of this as the "reader" — it takes raw input and turns it into
# structured Python objects that the rest of the pipeline can work with.


import json
import os
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def parse_json_file(filepath):
    """
    Load a single paper from a JSON file.

    Each JSON file is expected to have fields like:
      - title
      - abstract
      - authors
      - year
      - doi

    Returns a dictionary with the paper's data, or None if the file can't be read.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def parse_text_abstract(text):
    """
    Parse a raw abstract string into a simple structured dict.

    This is useful when you only have plain text (e.g., copy-pasted from PubMed).
    Returns a dict with the abstract text cleaned up and ready for processing.
    """
    return {
        "abstract": text.strip(),
        "source": "plain_text",
    }


def extract_abstract_from_text(text):
    """
    Best-effort extraction of abstract text from a PDF's raw text.

    Looks for an 'Abstract' heading and captures text until a likely next section.
    Returns an empty string if no abstract section is found.
    """
    if not text:
        return ""

    normalized = re.sub(r"\r\n?", "\n", text)
    normalized = re.sub(r"[ \t]+", " ", normalized)

    pattern = re.compile(
        r"\bAbstract\b[:\s]*"
        r"(.*?)"
        r"(?=\n\s*(?:Keywords?|Introduction|Background|Methods?|Materials?|Results?|Discussion|Conclusion|References)\b)",
        re.IGNORECASE | re.DOTALL,
    )

    match = pattern.search(normalized)
    if match:
        return match.group(1).strip()

    return ""


def extract_year_from_text(text):
    """
    Best-effort extraction of publication year.
    Returns an int or None.
    """
    if not text:
        return None

    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    if not years:
        return None

    # Conservative: take the first plausible year found.
    return int(years[0])


def extract_doi_from_text(text):
    """
    Best-effort DOI extraction from raw text.
    """
    if not text:
        return ""

    match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", text, re.IGNORECASE)
    return match.group(0).strip() if match else ""


def parse_pdf_file(filepath):
    """
    Parse a single PDF paper into a structured dictionary.

    Returns a dictionary with fields aligned to the JSON schema used by parse_json_file(),
    or None if the PDF can't be read.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    if fitz is None:
        print("PyMuPDF is not installed. Install it with: pip install pymupdf")
        return None

    try:
        doc = fitz.open(filepath)
    except Exception as e:
        print(f"Could not open PDF '{filepath}': {e}")
        return None

    full_text = []
    for page in doc:
        try:
            full_text.append(page.get_text())
        except Exception:
            continue

    doc.close()

    text = "\n".join(full_text).strip()
    if not text:
        print(f"No extractable text found in PDF: {filepath}")
        return None

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    title = lines[0] if lines else os.path.splitext(os.path.basename(filepath))[0]
    abstract = extract_abstract_from_text(text)
    year = extract_year_from_text(text)
    doi = extract_doi_from_text(text)

    paper = {
        "title": title,
        "abstract": abstract,
        "authors": [],
        "year": year,
        "doi": doi,
        "source": "pdf",
        "source_file": os.path.basename(filepath),
        "full_text": text,
    }

    return paper


def save_paper_to_json(paper, output_filepath):
    """
    Save a parsed paper dictionary to JSON.
    """
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(paper, f, ensure_ascii=False, indent=2)


def load_papers_from_folder(folder_path):
    """
    Load all paper files from a given folder.

    Behavior:
      - If a .json exists, load it directly.
      - If a .pdf exists, parse it, save a sibling .json, and append the parsed paper.
    Returns a list of paper dictionaries.
    """
    papers = []

    if not os.path.isdir(folder_path):
        print(f"Folder not found: {folder_path}")
        return papers

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        if filename.endswith(".json"):
            paper = parse_json_file(filepath)
            if paper:
                papers.append(paper)

        elif filename.endswith(".pdf"):
            json_filepath = os.path.splitext(filepath)[0] + ".json"

            if os.path.exists(json_filepath):
                paper = parse_json_file(json_filepath)
            else:
                paper = parse_pdf_file(filepath)
                if paper:
                    save_paper_to_json(paper, json_filepath)

            if paper:
                papers.append(paper)

    print(f"Loaded {len(papers)} papers from '{folder_path}'.")
    return papers
