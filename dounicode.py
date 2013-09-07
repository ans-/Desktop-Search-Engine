import sys, re

def decode_heuristically(string, enc = None, denc = sys.getdefaultencoding()):
    if isinstance(string, unicode): return string, 0, "utf-8"
    try:
        new_string = unicode(string, "ascii")
        return string, 0, "ascii"
    except UnicodeError:
        encodings = ["utf-8","iso-8859-1","cp1252","iso-8859-15"]

        if denc != "ascii": encodings.insert(0, denc)

        if enc: encodings.insert(0, enc)

        for enc in encodings:
            if (enc in ("iso-8859-15", "iso-8859-1") and
                re.search(r"[\x80-\x9f]", string) is not None):
                continue

            if (enc in ("iso-8859-1", "cp1252") and
                re.search(r"[\xa4\xa6\xa8\xb4\xb8\xbc-\xbe]", string)\
                is not None):
                continue

            try:
                new_string = unicode(string, enc)
            except UnicodeError:
                pass
            else:
                if new_string.encode(enc) == string:
                    return new_string, 0, enc

        output = [(unicode(string, enc, "ignore"), enc) for enc in encodings]
        output = [(len(new_string[0]), new_string) for new_string in output]
        output.sort()
        new_string, enc = output[-1][1]
        return new_string, 1, enc
