# cleaner.py
# This module handles text cleaning and preprocessing.
# Raw text from papers often contains noise: extra whitespace, HTML tags,
# special characters, or inconsistent formatting.
# The functions here standardize the text so it's ready for analysis or tagging.
# Think of this as the "scrubber" — it tidies up messy text before we use it.

import re
import string


def remove_extra_whitespace(text):
    """
    Replace multiple spaces, tabs, or newlines with a single space.
    Strips leading and trailing whitespace from the result.
    """
    return re.sub(r"\s+", " ", text).strip()


def remove_special_characters(text, keep_punctuation=True):
    """
    Remove non-ASCII or unwanted special characters from text.

    If keep_punctuation is True, standard punctuation (.,!?-) is preserved.
    Otherwise, only alphanumeric characters and spaces are kept.
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and basic punctuation
        allowed = set(string.ascii_letters + string.digits + string.punctuation + " ")
        return "".join(c for c in text if c in allowed)
    else:
        return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def lowercase_text(text):
    """
    Convert all text to lowercase.
    Useful for case-insensitive keyword matching.
    """
    return text.lower()


def clean_abstract(abstract):
    """
    Apply a full cleaning pipeline to a paper abstract.

    Steps:
      1. Remove extra whitespace
      2. Remove special characters (keeping punctuation)
      3. Lowercase the text

    Returns the cleaned abstract string.
    """
    text = remove_extra_whitespace(abstract)
    text = remove_special_characters(text, keep_punctuation=True)
    text = lowercase_text(text)
    return text


def clean_paper(paper):
    """
    Clean all relevant text fields in a paper dictionary.

    Expects a dict with at least an 'abstract' key.
    Returns the same dict with cleaned text fields.
    """
    if "abstract" in paper and paper["abstract"]:
        paper["abstract"] = clean_abstract(paper["abstract"])

    if "title" in paper and paper["title"]:
        paper["title"] = remove_extra_whitespace(paper["title"])

    return paper
