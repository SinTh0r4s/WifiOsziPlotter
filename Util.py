def to_one_decimal(value: float) -> str:
    return "%.1f" % value


def get_bytes_per_sample(bits: int) -> int:
    if bits <= 8:
        return 1
    if bits <= 16:
        return 2
    if bits <= 24:
        return 3
    return 4
