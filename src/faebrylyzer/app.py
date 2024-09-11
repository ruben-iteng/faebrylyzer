# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module, Node
from faebryk.libs.brightness import TypicalLuminousIntensity
from faebryk.libs.library import L
from faebryk.libs.units import P

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


# TODO: move elsewhere
def set_capacitance_for_decoupling_capacitors(node: Node, capacitance: F.Constant):
    for n in node.get_children(direct_only=False, types=Module):
        if n.has_trait(F.is_decoupled):
            _capacitance = n.get_trait(F.is_decoupled).get_capacitor().capacitance
            if isinstance(_capacitance.get_most_narrow(), F.TBD):
                capacitance.merge(capacitance)


def set_resistance_for_pull_resistors(node: Node, resistance: F.Constant):
    for n in node.get_children(direct_only=False, types=Module):
        if n.has_trait(F.ElectricLogic.has_pulls):
            resistors = n.get_trait(F.ElectricLogic.has_pulls).get_pulls()
            if resistors:
                for r in resistors:
                    if r:
                        if isinstance(r.resistance.get_most_narrow(), F.TBD):
                            r.resistance.merge(resistance)


class faebrylyzerApp(Module):
    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    power_led = L.f_field(F.PoweredLED)(low_side_resistor=False)
    status_led = L.f_field(F.PoweredLED)(low_side_resistor=False)
    channel_leds = L.list_field(2, lambda: F.PoweredLED(low_side_resistor=False))
    ldo: F.LDO
    faebrylyzer_module: faebrylyzerModule
    mcu: F.CBM9002A_56ILG_Reference_Design
    buffer: F.SNx4LVC541A
    eeprom: F.EEPROM
    input_current_limiting_resistor = L.list_field(2, ResistorArray)
    mcu_current_limiting_resistor = L.list_field(2, ResistorArray)
    input_pullup_resistor = L.list_field(2, ResistorArray)
    # usb_protection = L.f_field(F.GenericBusProtection)(F.USB2_0)
    faebryk_logo: faebrykLogo

    def __preinit__(self):
        # ----------------------------------------
        #                aliases
        # ----------------------------------------
        usb = self.faebrylyzer_module.usb
        vbus = usb.usb_if.buspower
        v3_3 = self.ldo.power_out
        gnd = vbus.lv
        i2c = self.mcu.i2c
        # ----------------------------------------
        #                net names
        # ----------------------------------------
        nets = {
            "vbus": vbus.hv,
            "3v3": v3_3.hv,
            "gnd": gnd,
            "usb_P": usb.usb_if.d.p,
            "usb_N": usb.usb_if.d.n,
            "sda": i2c.sda.signal,
            "scl": i2c.scl.signal,
        }
        # rename logic channel nets
        for i, channel in enumerate(self.faebrylyzer_module.channels):
            nets[f"ch_{i}"] = channel.signal
        # rename buffer in and output channel nets and mcu input channel nets
        for i, channel in enumerate(self.buffer.Y):
            nets[f"buffer_out_{i}"] = channel.signal
        for i, channel in enumerate(self.buffer.A):
            nets[f"buffer_in_{i}"] = channel.signal
        for i, channel in enumerate(self.mcu.PB):
            nets[f"mcu_logic_{i}"] = self.mcu.PB[i].signal

        for net_name, mif in nets.items():
            assert isinstance(
                mif, F.Electrical
            ), f"You are trying to give a non-electrical interface: {mif}, a net name: {net_name}"  # noqa E501
            net = F.Net()
            net.add_trait(F.has_overriden_name_defined(net_name))
            net.part_of.connect(mif)

        # ----------------------------------------
        #              connections
        # ----------------------------------------
        # power connections
        self.ldo.power_in.connect(vbus)
        self.mcu.avcc.connect(v3_3)
        self.mcu.vcc.connect(v3_3)
        self.buffer.power.connect(v3_3)
        self.eeprom.power.connect(v3_3)

        # tvs protection
        self.ldo.power_in.get_trait(F.can_be_surge_protected).protect()
        v3_3.get_trait(F.can_be_surge_protected).protect()
        # usb.connect_via(self.usb_protection, self.mcu.usb)
        usb.connect(self.mcu.usb)

        # MCU status LED
        self.mcu.PA[1].signal.connect_via(self.status_led, gnd)
        # channel leds (only channel 0 and 1 get an indicator LED)
        for i, led in enumerate(self.channel_leds):
            self.buffer.Y[i].signal.connect_via(led, gnd)
            led.power.voltage.merge(v3_3.voltage)  # TODO remove
        # power indicator LED
        self.power_led.power.connect(vbus)

        # eeprom
        i2c.connect(self.eeprom.i2c)
        self.eeprom.write_protect.set(on=False)  # Disable write protection
        self.eeprom.set_address(0x00)

        # logic channels on connector to buffer via current limiting resistor
        # and pull-up
        for i, channel in enumerate(self.faebrylyzer_module.channels):
            channel.signal.connect_via(
                self.input_current_limiting_resistor[i // 4].resistor[3 - i % 4],
                self.buffer.A[i].signal,
            )
            self.buffer.A[i].signal.connect_via(
                self.input_pullup_resistor[i // 4].resistor[3 - i % 4],
                v3_3.hv,
            )

        # buffer to mcu via current limiting resistor
        for i, channel in enumerate(self.buffer.Y):
            channel.signal.connect_via(
                self.mcu_current_limiting_resistor[i // 4].resistor[3 - i % 4],
                self.mcu.PB[i].signal,
            )

        # enable pins of buffer
        for oe in self.buffer.OE:
            oe.signal.connect(gnd)

        # enable mcu
        self.mcu.wakeup.set(on=True)

        # ----------------------------------------
        #              parametrization
        # ----------------------------------------
        # current limiting resistors
        for ra in self.input_current_limiting_resistor:
            ra.resistance.merge(F.Constant(100 * P.ohm))
        for ra in self.mcu_current_limiting_resistor:
            ra.resistance.merge(F.Constant(100 * P.ohm))
        for ra in self.input_pullup_resistor:
            ra.resistance.merge(F.Constant(100 * P.kohm))

        # led colors and brightness
        self.power_led.led.color.merge(
            F.LED.Color.YELLOW
        )  # TypicalColorsByWavelength.RED)
        self.power_led.led.brightness.merge(
            TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
        )
        self.status_led.led.color.merge(
            F.LED.Color.GREEN
        )  # TypicalColorsByWavelength.YELLOW)
        self.status_led.led.brightness.merge(
            TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
        )

        for led in self.channel_leds:
            led.led.color.merge(F.LED.Color.GREEN)  # TypicalColorsByWavelength.GREEN)
            led.led.brightness.merge(
                TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
            )

        # ldo parameters
        self.ldo.output_voltage.merge(F.Constant(3.3 * P.V))
        self.ldo.output_current.merge(F.Constant(250 * P.mA))

        # eeprom parameters
        self.eeprom.memory_size.merge(F.Constant(256 * P.kB))

        # TODO remove this ----------------------------------------
        # for cap in self.mcu.oscillator.capacitors:
        #    cap.capacitance.merge(F.Constant(15 * P.pF))
        self.status_led.power.voltage.merge(v3_3.voltage)
        # TODO remove this ----------------------------------------

        set_capacitance_for_decoupling_capacitors(self, F.Constant(100 * P.nF))
        set_resistance_for_pull_resistors(self, F.Constant(3.3 * P.kohm))

        # ----------------------------------------
        #              specializations
        # ----------------------------------------
        # TODO: specialize single resistors into resistor arrays
