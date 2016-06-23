def bold(text):
    return "**{}**".format(text)


def box(text, lang=""):
    ret = "```{}\n{}\n```".format(lang, text)
    return ret


def inline(text):
    return "`{}`".format(text)


def italics(text):
    return "*{}*".format(text)


def pagify(text, delims=[], escape=True, shorten_by=8):
    """DOES NOT RESPECT MARKDOWN BOXES OR INLINE CODE"""
    in_text = text
    while len(in_text) > 2000:
        closest_delim = max([in_text.rfind(d, 0, 2000 - shorten_by)
                             for d in delims])
        closest_delim = closest_delim if closest_delim != -1 else 2000
        if escape:
            to_send = escape_mass_mentions(in_text[:closest_delim])
        else:
            to_send = in_text[:closest_delim]
        yield to_send
        in_text = in_text[closest_delim:]

    if escape:
        yield escape_mass_mentions(in_text)
    else:
        yield in_text


def strikethrough(text):
    return "~~{}~~".format(text)


def underline(text):
    return "__{}__".format(text)


def escape_mass_mentions(text):
    words = {
        "@everyone": "@\u200beveryone",
        "@here": "@\u200bhere"
    }
    for k, v in words.items():
        text = text.replace(k, v)
    return text
