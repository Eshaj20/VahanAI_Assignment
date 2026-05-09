from __future__ import annotations

import re

# This file contains functions for normalizing text, especially for handling Devanagari script.
NON_ALNUM_RE = re.compile(r"[^a-z0-9\s]")
SPACE_RE = re.compile(r"\s+")
DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

INDEPENDENT_VOWELS = {
    "अ": "a",
    "आ": "aa",
    "इ": "i",
    "ई": "ii",
    "उ": "u",
    "ऊ": "uu",
    "ऋ": "ri",
    "ए": "e",
    "ऐ": "ai",
    "ओ": "o",
    "औ": "au",
}

CONSONANTS = {
    "क": "k",
    "ख": "kh",
    "ग": "g",
    "घ": "gh",
    "ङ": "ng",
    "च": "ch",
    "छ": "chh",
    "ज": "j",
    "झ": "jh",
    "ञ": "ny",
    "ट": "t",
    "ठ": "th",
    "ड": "d",
    "ढ": "dh",
    "ण": "n",
    "त": "t",
    "थ": "th",
    "द": "d",
    "ध": "dh",
    "न": "n",
    "प": "p",
    "फ": "ph",
    "ब": "b",
    "भ": "bh",
    "म": "m",
    "य": "y",
    "र": "r",
    "ल": "l",
    "व": "v",
    "श": "sh",
    "ष": "sh",
    "स": "s",
    "ह": "h",
    "ळ": "l",
    "क़": "q",
    "ख़": "kh",
    "ग़": "g",
    "ज़": "z",
    "ड़": "r",
    "ढ़": "rh",
    "फ़": "f",
}

MATRAS = {
    "ा": "aa",
    "ि": "i",
    "ी": "ii",
    "ु": "u",
    "ू": "uu",
    "ृ": "ri",
    "े": "e",
    "ै": "ai",
    "ो": "o",
    "ौ": "au",
    "ं": "n",
    "ँ": "n",
    "ः": "h",
}

SPECIALS = {
    "ं": "n",
    "ँ": "n",
    "ः": "h",
    "्": "",
}


# This is a simple transliteration function that converts Devanagari script to Latin script. It handles independent vowels, consonants with and without matras, and special characters. It does not handle all possible combinations or nuances of the script, but it should work for basic text normalization purposes.
def transliterate_devanagari(text: str) -> str:
    output: list[str] = []
    chars = list(text)
    i = 0
    while i < len(chars):
        char = chars[i]

        if char in INDEPENDENT_VOWELS:
            output.append(INDEPENDENT_VOWELS[char])
            i += 1
            continue

        if char in CONSONANTS:
            base = CONSONANTS[char]
            next_char = chars[i + 1] if i + 1 < len(chars) else ""

            if next_char == "्":
                output.append(base)
                i += 2
                continue

            if next_char in MATRAS:
                output.append(base + MATRAS[next_char])
                i += 2
                continue

            output.append(base + "a")
            i += 1
            continue

        if char in SPECIALS:
            output.append(SPECIALS[char])
            i += 1
            continue

        output.append(char)
        i += 1

    return "".join(output)

# This function normalizes text by first checking for Devanagari characters and transliterating them if found. Then it converts the text to lowercase, replaces "&" with "and", removes non-alphanumeric characters, collapses multiple spaces into one, and trims leading/trailing whitespace.
def normalize_text(text: str) -> str:
    if DEVANAGARI_RE.search(text):
        text = transliterate_devanagari(text)
    text = text.lower().strip()
    text = text.replace("&", " and ")
    text = NON_ALNUM_RE.sub(" ", text)
    text = SPACE_RE.sub(" ", text)
    return text.strip()

# This function normalizes locality names by first normalizing the text and then applying specific replacements for common abbreviations like "kr", "hsr", and "btm". If the normalized text matches one of the keys in the replacements dictionary, it returns the corresponding value; otherwise, it returns the normalized text as is.
def normalize_locality(locality: str) -> str:
    text = normalize_text(locality)
    replacements = {
        "kr": "k r",
        "hsr": "h s r",
        "btm": "b t m",
    }
    return replacements.get(text, text)
