# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L

logger = logging.getLogger(__name__)


class MountingSlot(Module):
    unnamed: F.Electrical

    designator_prefix = L.f_field(F.has_designator_prefix_defined)("H")

    @L.rt_field
    def footprint(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.unnamed,
            }
        )

    def __preinit__(self):
        self.footprint.attach(F.KicadFootprint("custom:MountingSlot", pin_names=["1"]))
