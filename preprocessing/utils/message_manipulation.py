import re

import emoji
import unicodedata


def standardize_message(s: str):
    """Standardizes a Whatsapp message string

    Standardizes the string by replacing escape characters and decode emojis to their corresponding aliases. Also
    removes unknown unicode characters and links.

    Args:
        s: the input string

    Returns:
        The standardized string
    """
    s = re.sub('https?://[^\s]+', "", s)
    s = re.sub(r"\.+", " . ", s)
    s = re.sub(r"\?+", " ? ", s)
    s = re.sub(r"\!+", " ! ", s)
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


def correct_message(s: str, correction_map: dict, smiley: bool = False):
    """Replaces smileys and typos in a string

    Takes the given correction map. Smileys are replaced by their corresponding emoji description. If the map
    contains a smiley of length 2 (e.g. ``:)`` or ``:D``) all variances of that smiley are replaced by the
    corresponding description (meaning ``:)`` replaces ``:)``, ``:-)``, ``:)))`` and ``:-))))``). Normal words are
    replaced by their given replacements.

    Args:
        s: the string
        correction_map: dictionary of patterns and replacements
        smiley: Whether the correction map holds smileys

    Returns:
        The corrected string
    """
    for word in correction_map:
        if smiley and len(word) == 2:
            pattern = re.compile(r"{}-*{}+".format(re.escape(word[0]), re.escape(word[1])))
        else:
            pattern = re.compile(r"{}".format(re.escape(word)))
        s = re.sub(pattern, " {} ".format(correction_map[word]), s)
    return s
