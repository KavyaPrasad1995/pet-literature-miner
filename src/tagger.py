# tagger.py
# This module tags papers with relevant labels based on their content.
# It scans titles and abstracts for keywords related to:
#   - PET tracers (e.g., FDG, PSMA, FLT, DOTATATE)
#   - Oncology topics (e.g., tumor, cancer, metastasis, staging)
# Think of this as the "labeler" — it reads cleaned text and assigns categories
# so papers can be filtered and grouped for analysis.

# -----------------------------------------------------------------------
# Keyword lists — you can expand these as needed for your research
# -----------------------------------------------------------------------

PET_TRACER_KEYWORDS = [
    "fdg",
    "18f-fdg",
    "psma",
    "flt",
    "dotatate",
    "dotatoc",
    "fmiso",
    "fluciclovine",
    "choline",
    "amyloid",
    "tau",
    "fluoride",
    "gallium-68",
    "ga-68",
    "copper-64",
    "cu-64",
    "zirconium-89",
    "zr-89",
    "18F-FDG PET",
    "patients undergoing FDG PET",
    "PET imaging with FDG",
    "FDG PET scans",
    "metabolic",
    "interquartile"
]

ONCOLOGY_KEYWORDS = [
    "cancer",
    "tumor",
    "tumour",
    "oncology",
    "malignancy",
    "malignant",
    "metastasis",
    "metastatic",
    "carcinoma",
    "lymphoma",
    "melanoma",
    "staging",
    "recurrence",
    "progression",
    "chemotherapy",
    "radiation therapy",
    "radiotherapy",
    "immunotherapy",
    "biopsy",
]


def find_matching_keywords(text, keyword_list):
    """
    Search for keywords from a list in the given text.

    Parameters:
        text (str): The text to search (should already be lowercased).
        keyword_list (list): A list of keyword strings to look for.

    Returns:
        list: Keywords from the list that were found in the text.
    """
    found = []
    for keyword in keyword_list:
        if keyword in text:
            found.append(keyword)
    return found


def tag_paper(paper):
    """
    Tag a single paper dictionary with PET tracer and oncology labels.

    Looks at both the 'title' and 'abstract' fields (if present).
    Adds two new keys to the paper dict:
        - 'pet_tracers': list of matched PET tracer keywords
        - 'oncology_tags': list of matched oncology keywords
        - 'is_pet_paper': True if any PET tracer keyword was found
        - 'is_oncology_paper': True if any oncology keyword was found

    Returns the updated paper dict.
    """
    # Combine title and abstract into one searchable text block
    combined_text = ""
    if "title" in paper and paper["title"]:
        combined_text += paper["title"] + " "
    if "abstract" in paper and paper["abstract"]:
        combined_text += paper["abstract"]

    # Lowercase for case-insensitive matching
    combined_text = combined_text.lower()

    # Find matching keywords
    pet_matches = find_matching_keywords(combined_text, PET_TRACER_KEYWORDS)
    oncology_matches = find_matching_keywords(combined_text, ONCOLOGY_KEYWORDS)

    # Add tags to the paper dict
    paper["pet_tracers"] = pet_matches
    paper["oncology_tags"] = oncology_matches
    paper["is_pet_paper"] = len(pet_matches) > 0
    paper["is_oncology_paper"] = len(oncology_matches) > 0

    return paper


def tag_all_papers(papers):
    """
    Tag a list of paper dictionaries.

    Parameters:
        papers (list): List of paper dicts (already cleaned).

    Returns:
        list: The same list with tags added to each paper.
    """
    tagged = [tag_paper(paper) for paper in papers]
    print(f"Tagged {len(tagged)} papers.")
    return tagged
