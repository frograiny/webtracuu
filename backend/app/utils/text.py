"""Text normalization helpers for Vietnamese search."""

import re
import unicodedata


def repair_mojibake(text: str) -> str:
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def remove_diacritics(text: str) -> str:
    text = repair_mojibake(text)
    text = text.replace("đ", "d").replace("Đ", "D")
    nfkd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def normalize_query(text: str) -> str:
    normalized = remove_diacritics(text).lower().strip()
    return re.sub(r"\s+", " ", normalized)
