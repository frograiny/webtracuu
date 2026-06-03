from typing import Iterable

LECTURER_AUDIENCE = "Giảng viên"
STUDENT_AUDIENCE = "Sinh viên"
ALL_AUDIENCES = (LECTURER_AUDIENCE, STUDENT_AUDIENCE)

_STUDENT_KEYWORDS = (
    "sinh viên",
    "hoc sinh",
    "học sinh",
    "student",
)


def normalize_target_audience(value: str | None) -> str:
    if not value:
        return LECTURER_AUDIENCE

    normalized_value = value.strip().lower()
    if any(keyword in normalized_value for keyword in _STUDENT_KEYWORDS):
        return STUDENT_AUDIENCE

    return LECTURER_AUDIENCE


def normalize_target_audience_options(values: Iterable[str | None]) -> list[str]:
    normalized_values = {normalize_target_audience(value) for value in values if value is not None}
    ordered_values = [audience for audience in ALL_AUDIENCES if audience in normalized_values]
    return ["Tất cả", *ordered_values]
