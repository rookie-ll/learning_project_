def isbn_or_key(p):
    key_or_isbn = "key"
    w = p.replace("-", "")
    if len(p) == 13 and p.isdigit():
        key_or_isbn = "isbn"
    elif len(p) == 10 and w.isdigit():
        key_or_isbn = "isbn"
    return key_or_isbn
