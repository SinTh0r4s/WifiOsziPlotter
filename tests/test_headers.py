import pytest
import sys
# Add project folder to import path
sys.path.insert(0, '../osziplotter')

from osziplotter.network.Headers import BeaconHeader, CommandHeader, SampleTransmissionHeader


def mismatch_message(header1, header2):
    return "Header objects don't match.\nOriginal header: "\
           + str(header1.__dict__) + "\nParsed copy:     " + str(header2.__dict__)


def test_headers():
    """
    set values for every field which is translated to the binary
    header. Then convert those values to the binary header and
    back. If the result is equal to the original object the test
    is passed
    """

    # BEACON_HEADER
    beacon = BeaconHeader()
    beacon.beaconId = 11
    beacon.v_ref = 3300
    beacon.port = 12345
    beacon.num_samples = 10000
    beacon.num_channels = 1
    beacon.frequency = 100000
    beacon.resolution = 8
    beacon.model = "Leona OTP FTW"
    beacon.num_channels = 1
    beacon.uid = 5433
    beacon.adc = "Just kidding"

    beacon_bin = beacon.to_bytearray()
    beacon_copy = BeaconHeader()
    beacon_copy.from_bytearray(beacon_bin)

    assert beacon.__dict__ == pytest.approx(beacon_copy.__dict__), mismatch_message(beacon, beacon_copy)

    # COMMAND_HEADER
    command = CommandHeader()
    command.port = 1234
    command.active = 1
    command.trigger_voltage = 600
    command.channel = 1

    command_bin = command.to_bytearray()
    command_copy = CommandHeader()
    command_copy.from_bytearray(command_bin)

    assert command.__dict__ == pytest.approx(command_copy.__dict__), mismatch_message(command, command_copy)

    # SAMPLE_TRANSMISSION_HEADER
    samples = SampleTransmissionHeader()
    samples.num_samples = 1
    samples.v_ref = 3300
    samples.channels = 1
    samples.resolution = 8
    samples.frequency = 100000
    samples.transmission_group_id = 123
    samples.num_frames = 1
    samples.frame_id = 0
    samples.payload = bytearray(1)

    samples_bin = samples.to_bytearray()
    samples_copy = SampleTransmissionHeader()
    samples_copy.from_bytearray(samples_bin)

    assert samples.__dict__ == pytest.approx(samples_copy.__dict__), mismatch_message(samples, samples_copy)


if __name__ == "__main__":
    test_headers()
    print("Tests successful!")
