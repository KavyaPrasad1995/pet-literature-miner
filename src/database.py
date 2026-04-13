# database.py
# This module handles saving and loading paper data to/from a local SQLite database.
# SQLite is a lightweight, file-based database — no server setup needed.
# It's a great choice for a beginner project because everything lives in one .db file.
# Think of this as the "storage room" — processed papers go in, and you can
# query them back out later for analysis.

import sqlite3
import json
import os


# Default path for the database file (stored in the data/ folder)
DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "papers.db"
)


def get_connection(db_path=DEFAULT_DB_PATH):
    """
    Open a connection to the SQLite database.

    Creates the database file if it doesn't already exist.
    Returns a sqlite3 Connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Lets us access columns by name
    return conn


def create_table(conn):
    """
    Create the 'papers' table if it doesn't already exist.

    Columns:
        - id: Auto-incrementing primary key
        - title: Paper title
        - abstract: Full abstract text
        - authors: Author list (stored as a JSON string)
        - year: Publication year
        - doi: Digital Object Identifier (unique paper ID)
        - pet_tracers: Matched PET tracer keywords (stored as JSON string)
        - oncology_tags: Matched oncology keywords (stored as JSON string)
        - is_pet_paper: 1 if tagged as a PET paper, 0 otherwise
        - is_oncology_paper: 1 if tagged as an oncology paper, 0 otherwise
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            abstract TEXT,
            authors TEXT,
            year INTEGER,
            doi TEXT UNIQUE,
            pet_tracers TEXT,
            oncology_tags TEXT,
            is_pet_paper INTEGER DEFAULT 0,
            is_oncology_paper INTEGER DEFAULT 0
        )
    """)
    conn.commit()


def insert_paper(conn, paper):
    """
    Insert a single paper into the database.

    Skips the paper if a record with the same DOI already exists.

    Parameters:
        conn: An active SQLite connection.
        paper (dict): A paper dictionary (after cleaning and tagging).
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO papers
            (title, abstract, authors, year, doi, pet_tracers, oncology_tags,
             is_pet_paper, is_oncology_paper)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            paper.get("title"),
            paper.get("abstract"),
            json.dumps(paper.get("authors", [])),  # Store list as JSON string
            paper.get("year"),
            paper.get("doi"),
            json.dumps(paper.get("pet_tracers", [])),
            json.dumps(paper.get("oncology_tags", [])),
            int(paper.get("is_pet_paper", False)),
            int(paper.get("is_oncology_paper", False)),
        ))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting paper: {e}")


def insert_all_papers(conn, papers):
    """
    Insert a list of papers into the database.

    Parameters:
        conn: An active SQLite connection.
        papers (list): List of paper dicts (cleaned and tagged).
    """
    for paper in papers:
        insert_paper(conn, paper)
    print(f"Inserted {len(papers)} papers into the database.")


def fetch_all_papers(conn):
    """
    Retrieve all papers from the database.

    Returns a list of sqlite3.Row objects (accessible like dicts).
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM papers")
    return cursor.fetchall()


def fetch_pet_papers(conn):
    """
    Retrieve only papers that were tagged as PET-related.

    Returns a list of sqlite3.Row objects.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM papers WHERE is_pet_paper = 1")
    return cursor.fetchall()


def fetch_oncology_papers(conn):
    """
    Retrieve only papers tagged as oncology-related.

    Returns a list of sqlite3.Row objects.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM papers WHERE is_oncology_paper = 1")
    return cursor.fetchall()
