# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.exporters.pcb.layout.absolute import LayoutAbsolute
from faebryk.exporters.pcb.layout.typehierarchy import LayoutTypeHierarchy
from faebryk.libs.library import L

from faebrylyzer.library.MountingSlot import MountingSlot
from faebrylyzer.library.SFPEdgeConnector import SFPEdgeConnector

logger = logging.getLogger(__name__)


class faebrylyzerModule(Module):
    cardedge_connector: SFPEdgeConnector
    keys: MountingSlot

    usb: F.USB2_0
    channels = L.list_field(8, F.ElectricLogic)

    # traits
    @L.rt_field
    def pcb_layout(self):
        Point = F.has_pcb_position.Point
        L = F.has_pcb_position.layer_type
        LVL = LayoutTypeHierarchy.Level

        layouts = [
            LVL(
                mod_type=MountingSlot,
                layout=LayoutAbsolute(Point((0, 0, 0, L.NONE))),
            ),
            LVL(
                mod_type=SFPEdgeConnector,
                layout=LayoutAbsolute(Point((0, 45, 0, L.NONE))),
            ),
        ]

        return F.has_pcb_layout_defined(LayoutTypeHierarchy(layouts))

    def __preinit__(self):
        # aliases
        vbus = self.usb.usb_if.buspower
        gnd = vbus.lv

        # connections
        # power
        for gnd_pin in [0, 9, 10, 13, 16, 19]:
            gnd.connect(self.cardedge_connector.unnamed[gnd_pin])
        for power_pin in [14, 15]:
            vbus.hv.connect(self.cardedge_connector.unnamed[power_pin])
        # channels
        for i, channel in enumerate(self.channels):
            if i == 0:
                self.cardedge_connector.unnamed[18].connect(channel.signal)
            else:
                self.cardedge_connector.unnamed[i].connect(channel.signal)
        # usb
        self.usb.usb_if.d.p.connect(self.cardedge_connector.unnamed[12])
        self.usb.usb_if.d.n.connect(self.cardedge_connector.unnamed[11])
