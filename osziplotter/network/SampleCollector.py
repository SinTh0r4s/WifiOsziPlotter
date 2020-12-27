from osziplotter.network.SampleGroup import SampleGroup
from osziplotter.network.Headers import SampleTransmissionHeader
from osziplotter.modelcontroller.PlotEvents import PlotEvents

from typing import Dict


class SampleCollector(PlotEvents):

    def __init__(self):
        super(SampleCollector, self).__init__()
        self.groups: Dict[int, SampleGroup] = {}

    def process_received_sample_transmission_header(self, header: SampleTransmissionHeader) -> None:
        self.__handle_timeout()
        if header.transmission_group_id not in self.groups:
            self.groups[header.transmission_group_id] = SampleGroup(header)
        if self.groups[header.transmission_group_id].add_packet(header):
            if self.groups[header.transmission_group_id].is_complete():
                self.put(self.groups[header.transmission_group_id].get_samples())
                self.groups.pop(header.transmission_group_id)

    def __handle_timeout(self) -> None:
        for groupId in self.groups:
            if self.groups[groupId].timeout():
                self.groups.pop(groupId)
