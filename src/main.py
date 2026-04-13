# main.py
# This is the entry point for the PET Literature Miner pipeline.
# It ties together all the modules:
#   1. parser.py  — loads paper data from files
#   2. cleaner.py — cleans and normalizes the text
#   3. tagger.py  — tags papers with PET tracer and oncology keywords
#   4. database.py — saves results to a local SQLite database
#
# To run the full pipeline, simply execute:
#   python src/main.py

import os
import sys

# Make sure Python can find the other modules in this folder
sys.path.insert(0, os.path.dirname(__file__))

from parser import load_papers_from_folder
from cleaner import clean_paper
from tagger import tag_all_papers
from database import get_connection, create_table, insert_all_papers, fetch_pet_papers

# -----------------------------------------------------------------------
# Configuration — update these paths as needed
# -----------------------------------------------------------------------

# Folder where your raw paper files are stored (PDFs or pre-parsed JSON)
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")

# Path to the SQLite database file
DB_PATH = os.path.join(DATA_FOLDER, "papers.db")


def run_pipeline():
    """
    Run the full literature mining pipeline.

    Steps:
        1. Load papers from the data/ folder
        2. Clean each paper's text
        3. Tag each paper with PET and oncology keywords
        4. Save results to the SQLite database
        5. Print a summary of what was found
    """
    print("=" * 50)
    print("PET Literature Miner — Starting Pipeline")
    print("=" * 50)

    # Step 1: Load papers
    print("\n[1/4] Loading papers...")
    papers = load_papers_from_folder(DATA_FOLDER)

    if not papers:
        print("No papers found. Add PDF or JSON files to the data/ folder and try again.")
        return

    # Step 2: Clean papers
    print("\n[2/4] Cleaning paper text...")
    papers = [clean_paper(paper) for paper in papers]
    print(f"Cleaned {len(papers)} papers.")

    # Step 3: Tag papers
    print("\n[3/4] Tagging papers with keywords...")
    papers = tag_all_papers(papers)

    # Step 4: Save to database
    print("\n[4/4] Saving to database...")
    conn = get_connection(DB_PATH)
    create_table(conn)
    insert_all_papers(conn, papers)

    # Summary
    pet_papers = fetch_pet_papers(conn)
    conn.close()

    print("\n" + "=" * 50)
    print("Pipeline Complete!")
    print(f"  Total papers processed : {len(papers)}")
    print(f"  PET-related papers     : {len(pet_papers)}")
    print(f"  Database saved at      : {DB_PATH}")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()
