

def convert(code_decimal):
    hexadecimal = hex(code_decimal >> 1)[2:]
    return hexadecimal


if __name__ == "__main__":
    print(hex(15705636909))
    print(bin(15705636909))
    print(convert(15705636909))
