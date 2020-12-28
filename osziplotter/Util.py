from typing import Tuple
from time import localtime


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


def get_frequency_readable(frequency: int) -> Tuple[int, str]:
    frequency_unit = "Hz"
    if frequency > 1000:
        frequency /= 1000
        frequency_unit = "kHz"
    if frequency > 1000:
        frequency /= 1000
        frequency_unit = "MHz"
    if frequency > 1000:
        frequency /= 1000
        frequency_unit = "GHz"
    return frequency, frequency_unit


def get_timestamp_readable(time: float) -> str:
    local_time = localtime(time)
    return str(local_time.tm_hour) + ":" + str(local_time.tm_min) + ":" + str(local_time.tm_sec)


def get_timesteps_readable(time: float) -> Tuple[float, str]:
    time_unit = "sec"
    if time < 1.0:
        time *= 1000
        time_unit = "ms"
    if time < 1.0:
        time *= 1000
        time_unit = "µs"
    if time < 1.0:
        time *= 1000
        time_unit = "ns"
    return time, time_unit
