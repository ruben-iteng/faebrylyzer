# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L

logger = logging.getLogger(__name__)


class faebrykLogo(Module):
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("LOGO")

    @L.rt_field
    def can_attach_to_footprint(self):
        return F.can_attach_to_footprint_via_pinmap(pinmap={})

    def __preinit__(self):
        F.can_attach_to_footprint().attach(
            F.KicadFootprint("custom:faebryk_logo", pin_names=[])
        )
