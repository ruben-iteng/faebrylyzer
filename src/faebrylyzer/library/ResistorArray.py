# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L
from faebryk.libs.units import Quantity
from faebryk.libs.util import times

logger = logging.getLogger(__name__)


class ResistorArray(Module):
    resistance: F.TBD[Quantity]
    rated_power: F.TBD[Quantity]
    rated_voltage: F.TBD[Quantity]

    resistor = L.list_field(4, F.Resistor)

    designator_prefix = L.f_field(F.has_designator_prefix_defined)("R")
