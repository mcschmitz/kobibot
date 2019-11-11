import re

import emoji
import unicodedata


def standardize_message(s: str):
    """Standardizes a Whatsapp message string

    Standardizes the string by replacing escape characters and decode emojis to their corresponding aliases. Also
    removes unknown unicode characters.

    Args:
        s: the input string

    Returns:
        The standardized string
    """
    s = "".join([s_i for s_i in s if unicodedata.category(s_i) != "Co"])
    s = s.strip()
    s = re.sub("\x00", "", s)
    if len(s) > 0:
        s = "".join([s_i for s_i in s if "MODIFIER FITZPATRICK" not in unicodedata.name(s_i)])
    s = s.strip()
    s = unicodedata.normalize("NFD", s)
    s = emoji.demojize(s)
    s = re.sub(r"(:[\w-]*:)", r" \1 ", s)
    s = " ".join(s.split())
    return s
