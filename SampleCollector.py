from SampleGroup import SampleGroup
from Headers import SampleTransmissionHeader
from typing import Callable


class SampleCollector:

    def __init_(self, draw_callback: Callable):
        self.groups: dict[int, SampleGroup] = {}
        self.__draw_callback = draw_callback

    def process_received_sample_transmission_header(self, header: SampleTransmissionHeader) -> None:
        self.__handle_timeout()
        if header.transmission_group_id not in self.groups:
            self.groups[header.transmission_group_id] = SampleGroup(header)
        if self.groups[header.transmission_group_id].add_packet(header):
            if self.groups[header.transmission_group_id].is_complete():
                self.__draw_callback(self.groups[header.transmission_group_id].get_samples())
                self.groups.pop(header.transmission_group_id)

    def __handle_timeout(self) -> None:
        for groupId in self.groups:
            if self.groups[groupId].timeout():
                self.groups.pop(groupId)
