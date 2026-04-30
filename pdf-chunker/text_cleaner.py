import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r", "\n")

    # Join broken lines inside paragraphs
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove too many blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()