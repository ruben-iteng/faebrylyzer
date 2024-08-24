# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.core import Module, Node
from faebryk.core.util import (
    get_node_children_all,
)
from faebryk.libs.brightness import TypicalLuminousIntensity
from faebryk.libs.units import P
from faebryk.libs.util import times

from faebrylyzer.library.faebrykLogo import faebrykLogo
from faebrylyzer.library.faebrylyzerModule import faebrylyzerModule
from faebrylyzer.library.ResistorArray import ResistorArray

logger = logging.getLogger(__name__)

"""
This file is for the top-level application modules.
This should be the entrypoint for collaborators to start in to understand your project.
Treat it as the high-level design of your project.
Avoid putting any generic or reusable application modules here.
Avoid putting any low-level modules or parameter specializations here.
"""


class faebrylyzerApp(Module):
    def __init__(self) -> None:
        super().__init__()

        # TODO: move elsewhere
        def set_capacitance_for_decoupling_capacitors(
            node: Node, capacitance: F.Constant
        ):
            for n in get_node_children_all(node):
                if n.has_trait(F.is_decoupled):
                    _capacitance = (
                        n.get_trait(F.is_decoupled).get_capacitor().PARAMs.capacitance
                    )
                    if isinstance(_capacitance.get_most_narrow(), F.TBD):
                        capacitance.merge(capacitance)

        def set_resistance_for_pull_resistors(node: Node, resistance: F.Constant):
            for n in get_node_children_all(node):
                if n.has_trait(F.ElectricLogic.has_pulls):
                    resistors = n.get_trait(F.ElectricLogic.has_pulls).get_pulls()
                    if resistors:
                        for r in resistors:
                            if r:
                                if isinstance(
                                    r.PARAMs.resistance.get_most_narrow(), F.TBD
                                ):
                                    r.PARAMs.resistance.merge(resistance)

        # ----------------------------------------
        #     modules, interfaces, parameters
        # ----------------------------------------
        class _NODEs(Module.NODES()):
            power_led = F.PoweredLED(low_side_resistor=False)
            status_led = F.PoweredLED(low_side_resistor=False)
            channel_leds = times(2, lambda: F.PoweredLED(low_side_resistor=False))
            ldo = F.LDO()
            faebrylyzer_module = faebrylyzerModule()
            mcu = F.CBM9002A_56ILG_Reference_Design()
            buffer = F.SNx4LVC541A()
            eeprom = F.EEPROM()
            input_current_limiting_resistor = times(2, ResistorArray)
            mcu_current_limiting_resistor = times(2, ResistorArray)
            input_pullup_resistor = times(2, ResistorArray)
            usb_protection = F.GenericBusProtection(F.USB2_0)
            faebryk_logo = faebrykLogo()

        self.NODEs = _NODEs(self)

        class _PARAMs(Module.PARAMS()): ...

        self.PARAMs = _PARAMs(self)

        # ----------------------------------------
        #                aliases
        # ----------------------------------------
        usb = F.USB2_0()
        vbus = usb.IFs.usb_if.IFs.buspower
        v3_3 = self.NODEs.ldo.IFs.power_out
        gnd = vbus.IFs.lv
        i2c = self.NODEs.mcu.IFs.i2c
        # ----------------------------------------
        #                net names
        # ----------------------------------------
        nets = {
            "vbus": vbus.IFs.hv,
            "3v3": v3_3.IFs.hv,
            "gnd": gnd,
            "usb_P": usb.IFs.usb_if.IFs.d.IFs.p,
            "usb_N": usb.IFs.usb_if.IFs.d.IFs.n,
            "sda": i2c.IFs.sda.IFs.signal,
            "scl": i2c.IFs.scl.IFs.signal,
        }
        # rename logic channel nets
        for i, channel in enumerate(self.NODEs.faebrylyzer_module.IFs.channels):
            nets[f"ch_{i}"] = channel.IFs.signal
        # rename buffer in and output channel nets and mcu input channel nets
        for i, channel in enumerate(self.NODEs.buffer.IFs.Y):
            nets[f"buffer_out_{i}"] = channel.IFs.signal
        for i, channel in enumerate(self.NODEs.buffer.IFs.A):
            nets[f"buffer_in_{i}"] = channel.IFs.signal
        for i, channel in enumerate(self.NODEs.mcu.IFs.PB):
            nets[f"mcu_logic_{i}"] = self.NODEs.mcu.IFs.PB[i].IFs.signal

        for net_name, mif in nets.items():
            assert isinstance(
                mif, F.Electrical
            ), f"You are trying to give a non-electrical interface: {mif}, a net name: {net_name}"
            net = F.Net()
            net.add_trait(F.has_overriden_name_defined(net_name))
            net.IFs.part_of.connect(mif)

        # ----------------------------------------
        #              connections
        # ----------------------------------------
        # power connections
        self.NODEs.ldo.IFs.power_in.connect(vbus)
        self.NODEs.mcu.IFs.avcc.connect(v3_3)
        self.NODEs.mcu.IFs.vcc.connect(v3_3)
        self.NODEs.buffer.IFs.vcc.connect(v3_3)
        self.NODEs.eeprom.IFs.power.connect(v3_3)

        self.NODEs.faebrylyzer_module.IFs.usb.connect(usb)

        # tvs protection
        vbus.get_trait(F.can_be_surge_protected).protect()
        v3_3.get_trait(F.can_be_surge_protected).protect()
        usb.connect_via(self.NODEs.usb_protection, self.NODEs.mcu.IFs.usb)

        # MCU status LED
        self.NODEs.mcu.IFs.PA[1].IFs.signal.connect_via(self.NODEs.status_led, gnd)
        # channel leds (only channel 0 and 1 get an indicator LED)
        for i, led in enumerate(self.NODEs.channel_leds):
            self.NODEs.buffer.IFs.Y[i].IFs.signal.connect_via(led, gnd)
            led.IFs.power.PARAMs.voltage.merge(v3_3.PARAMs.voltage)
        # power indicator LED
        self.NODEs.power_led.IFs.power.connect(vbus)

        # eeprom
        i2c.connect(self.NODEs.eeprom.IFs.i2c)
        self.NODEs.eeprom.IFs.write_protect.set(on=False)  # Disable write protection
        self.NODEs.eeprom.set_address(0x00)

        # logic channels on connector to buffer via current limiting resistor
        # and pull-up
        for i, channel in enumerate(self.NODEs.faebrylyzer_module.IFs.channels):
            channel.IFs.signal.connect_via(
                self.NODEs.input_current_limiting_resistor[i // 4].NODEs.resistor[
                    3 - i % 4
                ],
                self.NODEs.buffer.IFs.A[i].IFs.signal,
            )
            self.NODEs.buffer.IFs.A[i].IFs.signal.connect_via(
                self.NODEs.input_pullup_resistor[i // 4].NODEs.resistor[3 - i % 4],
                v3_3.IFs.hv,
            )

        # buffer to mcu via current limiting resistor
        for i, channel in enumerate(self.NODEs.buffer.IFs.Y):
            channel.IFs.signal.connect_via(
                self.NODEs.mcu_current_limiting_resistor[i // 4].NODEs.resistor[
                    3 - i % 4
                ],
                self.NODEs.mcu.IFs.PB[i].IFs.signal,
            )

        # enable pins of buffer
        for oe in self.NODEs.buffer.IFs.OE:
            oe.IFs.signal.connect(gnd)

        # usb
        self.NODEs.mcu.IFs.usb.connect(self.NODEs.faebrylyzer_module.IFs.usb)

        # enable mcu
        self.NODEs.mcu.IFs.wakeup.set(on=True)

        # ----------------------------------------
        #              parametrization
        # ----------------------------------------
        # current limiting resistors
        for ra in self.NODEs.input_current_limiting_resistor:
            ra.PARAMs.resistance.merge(F.Constant(100 * P.ohm))
        for ra in self.NODEs.mcu_current_limiting_resistor:
            ra.PARAMs.resistance.merge(F.Constant(100 * P.ohm))
        for ra in self.NODEs.input_pullup_resistor:
            ra.PARAMs.resistance.merge(F.Constant(100 * P.kohm))

        # led colors and brightness
        self.NODEs.power_led.NODEs.led.PARAMs.color.merge(
            F.LED.Color.YELLOW
        )  # TypicalColorsByWavelength.RED)
        self.NODEs.power_led.NODEs.led.PARAMs.brightness.merge(
            TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
        )
        self.NODEs.status_led.NODEs.led.PARAMs.color.merge(
            F.LED.Color.GREEN
        )  # TypicalColorsByWavelength.YELLOW)
        self.NODEs.status_led.NODEs.led.PARAMs.brightness.merge(
            TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
        )

        for led in self.NODEs.channel_leds:
            led.NODEs.led.PARAMs.color.merge(
                F.LED.Color.GREEN
            )  # TypicalColorsByWavelength.GREEN)
            led.NODEs.led.PARAMs.brightness.merge(
                TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
            )

        # ldo parameters
        self.NODEs.ldo.PARAMs.output_voltage.merge(F.Constant(3.3 * P.V))
        self.NODEs.ldo.PARAMs.output_current.merge(F.Constant(250 * P.mA))

        # eeprom parameters
        self.NODEs.eeprom.PARAMs.memory_size.merge(F.Constant(256 * P.kB))

        # TODO remove this ----------------------------------------
        for cap in self.NODEs.mcu.NODEs.oscillator.NODEs.capacitors:
            cap.PARAMs.capacitance.merge(F.Constant(15 * P.pF))
        self.NODEs.status_led.IFs.power.PARAMs.voltage.merge(v3_3.PARAMs.voltage)
        # TODO remove this ----------------------------------------

        set_capacitance_for_decoupling_capacitors(self, F.Constant(100 * P.nF))
        set_resistance_for_pull_resistors(self, F.Constant(3.3 * P.kohm))

        # ----------------------------------------
        #              specializations
        # ----------------------------------------
        # TODO: packages single resistors as explicit resistor arrays
        # create a resistor array for every 4 resistors
        # for i, r in enumerate(self.NODEs.input_current_limiting_resistor):
        #    if i % 4 == 0:
        #        resistor_array = F.ResistorArray(num_resistors=4)
        #        for array_resistor, resistor in zip(
        #            resistor_array.NODEs.resistor,
        #            self.NODEs.input_current_limiting_resistor[i : i + 4],
        #        ):
        #            specialize_module(resistor, array_resistor)

        # self.NODEs.mcu_current_limiting_resistor_array = resistor_array
