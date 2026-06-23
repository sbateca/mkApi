def normalize_str(text: str | None) -> str:
    if text is None:
        return ""

    return text.strip().casefold()


def capitalize_str(text: str) -> str:
    if text is None:
        return ""

    return text.strip().capitalize()
