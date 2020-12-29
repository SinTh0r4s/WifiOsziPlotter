from osziplotter.network.SampleGroup import SampleGroup
from osziplotter.network.Headers import SampleTransmissionHeader
from osziplotter.modelcontroller.PlotEvents import PlotEvents

from typing import Dict


class SampleCollector(PlotEvents):

    def __init__(self) -> None:
        super(SampleCollector, self).__init__()
        self._groups: Dict[int, SampleGroup] = {}

    def process_received_sample_transmission_header(self, header: SampleTransmissionHeader) -> None:
        self._handle_timeout()
        if header.transmission_group_id not in self._groups:
            self._groups[header.transmission_group_id] = SampleGroup(header)
        if self._groups[header.transmission_group_id].add_packet(header):
            if self._groups[header.transmission_group_id].is_complete():
                self.put(self._groups[header.transmission_group_id].get_samples())
                self._groups.pop(header.transmission_group_id)

    def _handle_timeout(self) -> None:
        for groupId in self._groups:
            if self._groups[groupId].timeout():
                self._groups.pop(groupId)
                return
