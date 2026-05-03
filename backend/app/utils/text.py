"""Tiện ích xử lý văn bản Tiếng Việt cho tìm kiếm."""

import unicodedata


def remove_diacritics(text: str) -> str:
    """Loại bỏ dấu Tiếng Việt: 'vật liệu' → 'vat lieu'."""
    text = text.replace("đ", "d").replace("Đ", "D")
    nfkd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def normalize_query(text: str) -> str:
    """Chuẩn hóa query: bỏ dấu + lowercase + strip."""
    return remove_diacritics(text).lower().strip()
