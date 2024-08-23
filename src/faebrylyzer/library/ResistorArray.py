# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.core import Module
from faebryk.library.has_designator_prefix_defined import has_designator_prefix_defined
from faebryk.libs.units import Quantity
from faebryk.libs.util import times

logger = logging.getLogger(__name__)


class ResistorArray(Module):
    @classmethod
    def NODES(cls):
        # submodules
        class _NODES(super().NODES()):
            resistor = times(4, F.Resistor)

        return _NODES

    @classmethod
    def PARAMS(cls):
        # parameters
        class _PARAMS(super().PARAMS()):
            resistance = F.TBD[Quantity]()
            rated_power = F.TBD[Quantity]()
            rated_voltage = F.TBD[Quantity]()

        return _PARAMS

    @classmethod
    def IFS(cls):
        # interfaces
        class _IFS(super().IFS()):
            pass

        return _IFS

    def __init__(self):
        # boilerplate
        super().__init__()
        self.IFs = self.IFS()(self)
        self.PARAMs = self.PARAMS()(self)
        self.NODEs = self.NODES()(self)

        # connections

        # traits
        self.add_trait(has_designator_prefix_defined("R"))
