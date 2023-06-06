from unidecode import unidecode

COT = [
    #Sensitive data
]


def isCotisant(fn, ln):
    first = unidecode(fn).strip().upper()
    last = unidecode(ln).strip().upper()
    #return [last, first] in COT
    return True