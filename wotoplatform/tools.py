

# make_sure_num will make sure that when you convert `i`
# to string, its length be the exact same as `count`.
# it will append 0 to the left side of the number to do so.
# for example:
# make_sure_num(5, 8) will return "00000005"
def make_sure_num(i: int, count: int) -> str:
    s = str(i)
    while len(s) < count:
        s = '0' + s
    return s

# make_sure_byte is a useful function. consider b is a number in string
# and you are sending it as a byte to this function.
# this function then, will ensure that the length of this byte array
# is exactly equal to the passed-by argument.
# for example:
# make_sure_byte([]byte("5"), 8) will return []byte("5       ")
# the returned value's length will be exactly the same as length.
def make_sure_byte(b: bytes, length: int) -> bytes:
    tmp_b = b
    while len(b) < length:
        tmp_b = tmp_b + b' '
    return bytes(tmp_b, 'utf-8')