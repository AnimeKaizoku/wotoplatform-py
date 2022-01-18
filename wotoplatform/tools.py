

def make_sure_byte(b: bytes, length: int) -> bytes:
    """
    make_sure_byte is a useful function. consider b is a number in string
    and you are sending it as a byte to this function.
    this function then, will ensure that the length of this byte array
    is exactly equal to the passed-by argument.
    for example:
    make_sure_byte([]byte("5"), 8) will return []byte("5       ")
    the returned value's length will be exactly the same as length.
    """
    tmp_b = b
    while len(b) < length: tmp_b = tmp_b + b' '
    return bytes(tmp_b, 'utf-8')