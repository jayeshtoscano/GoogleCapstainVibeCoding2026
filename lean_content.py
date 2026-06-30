import re

from mongodb import load_collection


def remove_words(text, words):

    for word in sorted(words, key=len, reverse=True):

        pattern = r"\b" + re.escape(word) + r"\b"

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )

    return text


def LeanContent(prompt: str):

    fillers = load_collection("fillers")
    hedges = load_collection("hedges")
    gestures = load_collection("gestures")
    courtesy = load_collection("courtesy")

    cleaned = prompt

    cleaned = remove_words(cleaned, fillers)
    cleaned = remove_words(cleaned, hedges)
    cleaned = remove_words(cleaned, gestures)
    cleaned = remove_words(cleaned, courtesy)

    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()
