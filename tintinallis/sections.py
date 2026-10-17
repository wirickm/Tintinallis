"""Section names and their PDF page ranges."""

SECTIONS = {
    "Section 1": (20, 74),
    "Section 2": (74, 88),
    "Section 3": (88, 130),
    "Section 4": (130, 186),
    "Section 5": (186, 208),
    "Section 6": (208, 270),
    "Section 7": (270, 298),
    "Section 8": (298, 332),
    "Section 9": (332, 438),
    "Section 10": (438, 508),
    "Section 11": (508, 596),
    "Section 12": (596, 646),
    "Section 13": (646, 664),
    "Section 14": (664, 704),
    "Section 15": (704, 758),
    "Section 16": (758, 792),
    "Section 17": (792, 806),
    "Section 18": (806, 862),
    "Section 19": (862, 896),
    "Section 20": (896, 926),
    "Section 21": (926, 938),
    "Section 22": (938, 946),
    "Index": (946, None),  # None means to the end of the document
}


def slug(name):
    """
    Return a file-friendly name, e.g. "Section 1" -> "section_01".
    """
    if name not in SECTIONS:
        raise KeyError(f"Unknown section: {name}")
    if name == "Index":
        return "index"
    return f"section_{int(name.split()[-1]):02d}"


def page_range(name):
    """
    Return (start_page, end_page) for a section. end_page may be None.
    """
    if name not in SECTIONS:
        raise KeyError(f"Unknown section: {name}")
    return SECTIONS[name]
