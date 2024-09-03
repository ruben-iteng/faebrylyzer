# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L

logger = logging.getLogger(__name__)


class SFPEdgeConnector(Module):
    unnamed = L.list_field(20, F.Electrical)

    designator_prefix = L.f_field(F.has_designator_prefix_defined)("J")

    @L.rt_field
    def can_attach_to_footprint(self):
        return F.can_attach_to_footprint_via_pinmap(
            pinmap={f"{i+1}": self.unnamed[i] for i in range(20)}
        )

    def __preinit__(self):
        F.can_attach_to_footprint().attach(
            F.KicadFootprint("custom:SFP_Edge", pin_names=[f"{i+1}" for i in range(20)])
        )
