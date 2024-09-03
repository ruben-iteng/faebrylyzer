# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.picker.lcsc import LCSC_Part
from faebryk.libs.picker.picker import (
    PickerOption,
    has_part_picked_remove,
    pick_module_by_params,
)
from faebryk.libs.units import P

from faebrylyzer.library.faebrykLogo import faebrykLogo
from faebrylyzer.library.MountingSlot import MountingSlot
from faebrylyzer.library.ResistorArray import ResistorArray
from faebrylyzer.library.SFPEdgeConnector import SFPEdgeConnector

logger = logging.getLogger(__name__)

"""
This file is for picking actual electronic components for your design.
You can make use of faebryk's picker & parameter system to do this.
"""

# part pickers --------------------------------------------


def pick_resistor(resistor: F.Resistor):
    """
    Link a partnumber/footprint to a Resistor

    Selects only 1% 0402 resistors
    """

    pick_module_by_params(
        resistor,
        [
            PickerOption(
                part=LCSC_Part(partno="C25076"),
                params={"resistance": F.Constant(100 * P.ohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25087"),
                params={"resistance": F.Constant(200 * P.ohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C11702"),
                params={"resistance": F.Constant(1 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25879"),
                params={"resistance": F.Constant(2.2 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25890"),
                params={"resistance": F.Constant(3.3 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25900"),
                params={"resistance": F.Constant(4.7 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25905"),
                params={"resistance": F.Constant(5.1 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25917"),
                params={"resistance": F.Constant(6.8 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25744"),
                params={"resistance": F.Constant(10 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25752"),
                params={"resistance": F.Constant(12 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25771"),
                params={"resistance": F.Constant(27 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25741"),
                params={"resistance": F.Constant(100 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25782"),
                params={"resistance": F.Constant(390 * P.kohm)},
            ),
            PickerOption(
                part=LCSC_Part(partno="C25790"),
                params={"resistance": F.Constant(470 * P.kohm)},
            ),
        ],
    )


def pick_capacitor(module: F.Capacitor):
    """
    Link a partnumber/footprint to a Capacitor

    Uses 0402 when possible
    """

    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C1548"),
                params={
                    "temperature_coefficient": F.Constant(
                        F.Capacitor.TemperatureCoefficient.C0G,
                    ),
                    "capacitance": F.Constant(15 * P.pF),
                    "rated_voltage": F.Constant(50 * P.V),
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C1525"),
                params={
                    "temperature_coefficient": F.Constant(
                        F.Capacitor.TemperatureCoefficient.X7R,
                    ),
                    "capacitance": F.Constant(100 * P.nF),
                    "rated_voltage": F.Constant(16 * P.V),
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C52923"),
                params={
                    "temperature_coefficient": F.Constant(
                        F.Capacitor.TemperatureCoefficient.X5R,
                    ),
                    "capacitance": F.Constant(10e-7 * P.F),
                    "rated_voltage": F.Constant(25 * P.V),
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C19702"),
                params={
                    "temperature_coefficient": F.Constant(
                        F.Capacitor.TemperatureCoefficient.X5R,
                    ),
                    "capacitance": F.Constant(10e-6 * P.F),
                    "rated_voltage": F.Constant(10 * P.V),
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C7196"),
                params={
                    "temperature_coefficient": F.Constant(
                        F.Capacitor.TemperatureCoefficient.X5R,
                    ),
                    "capacitance": F.Constant(10e-5 * P.F),
                    "rated_voltage": F.Constant(10 * P.V),
                },
            ),
        ],
    )


def pick_led(module: F.LED):
    pick_module_by_params(
        module,
        [
            # TODO: use parameters to select the right part?
            # PickerOption(
            #    part=LCSC_Part(partno="C2286"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.GREEN),
            #        "max_brightness": F.Constant(285e-3),
            #        "forward_voltage": F.Constant(3.7),
            #        "max_current": F.Constant(100e-3),
            #    },
            #    pinmap={"1": module.cathode, "2": module.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C72041"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.BLUE),
            #        "max_brightness": F.Constant(28.5e-3),
            #        "forward_voltage": F.Constant(3.1),
            #        "max_current": F.Constant(100e-3),
            #    },
            #    pinmap={"1": module.cathode, "2": module.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C2290"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.WHITE),
            #        "max_brightness": F.Constant(520e-3),
            #        "forward_voltage": F.Constant(3.1),
            #        "max_current": F.Constant(60e-3),
            #    },
            #    pinmap={"2": module.cathode, "1": module.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C2296"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.YELLOW),
            #        "max_brightness": F.Constant(113e-3),
            #        "forward_voltage": F.Constant(2.1),
            #        "max_current": F.Constant(20e-3),
            #    },
            #    pinmap={"2": module.cathode, "1": module.anode},
            # ),
            # MHT151WDT
            PickerOption(
                part=LCSC_Part(partno="C401114"),
                params={
                    "color": F.Constant(F.LED.Color.YELLOW),
                    "max_brightness": F.Constant(900 * P.millicandela),
                    "forward_voltage": F.Constant(3.15 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # MHT151UGCT
            PickerOption(
                part=LCSC_Part(partno="C559120"),
                params={
                    "color": F.Constant(F.LED.Color.GREEN),
                    "max_brightness": F.Constant(1120 * P.millicandela),
                    "forward_voltage": F.Constant(3.05 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # XL-1606SURC
            PickerOption(
                part=LCSC_Part(partno="C965860"),
                params={
                    "color": F.Constant(F.LED.Color.RED),
                    "max_brightness": F.Constant(220 * P.millicandela),
                    "forward_voltage": F.Constant(2.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # XL-1606SYGC
            # PickerOption(
            #    part=LCSC_Part(partno="C965864"),
            #    params={
            #        "color": F.Constant(F.LED.Color.YELLOW),
            #        "max_brightness": F.Constant(130 * P.millicandela),
            #        "forward_voltage": F.Constant(2.4 * P.V),
            #        "max_current": F.Constant(20 * P.mA),
            #    },
            #    pinmap={"1": module.cathode, "2": module.anode},
            # ),
            # XL-1606UBC
            PickerOption(
                part=LCSC_Part(partno="C965865"),
                params={
                    "color": F.Constant(F.LED.Color.BLUE),
                    "max_brightness": F.Constant(260 * P.millicandela),
                    "forward_voltage": F.Constant(2.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # XL-1606UGC
            # PickerOption(
            #    part=LCSC_Part(partno="C965863"),
            #    params={
            #        "color": F.Constant(F.LED.Color.GREEN),
            #        "max_brightness": F.Constant(1100 * P.millicandela),
            #        "forward_voltage": F.Constant(3.4 * P.V),
            #        "max_current": F.Constant(20 * P.mA),
            #    },
            #    pinmap={"1": module.cathode, "2": module.anode},
            # ),
            # XL-1606UOC
            PickerOption(
                part=LCSC_Part(partno="C965861"),
                params={
                    "color": F.Constant(F.LED.Color.ORANGE),
                    "max_brightness": F.Constant(230 * P.millicandela),
                    "forward_voltage": F.Constant(2.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # XL-1606UWC
            PickerOption(
                part=LCSC_Part(partno="C965866"),
                params={
                    "color": F.Constant(
                        F.LED.Color.WARM_WHITE
                        # TypicalColorByTemperature.WARM_WHITE_FLUORESCENT_LED
                    ),
                    "max_brightness": F.Constant(1100 * P.millicandela),
                    "forward_voltage": F.Constant(3.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
        ],
    )


def pick_diode(module: F.Diode):
    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C2128"),
                params={
                    "forward_voltage": F.Range(715 * P.mV, 1.0 * P.V),
                    "max_current": F.Constant(300 * P.mA),
                    "current": F.Constant(150 * P.mA),
                    "reverse_working_voltage": F.Constant(100 * P.V),
                    "reverse_leakage_current": F.Constant(1 * P.uA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            )
        ],
    )


def pick_crystal(module: F.Crystal):
    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C388793"),
                params={
                    "frequency": F.Constant(24 * P.Mhertz),
                    "load_capacitance": F.Constant(10 * P.pF),
                    "equivalent_series_resistance": F.Constant(50 * P.ohm),
                    "shunt_capacitance": F.Constant(5 * P.pF),
                    "frequency_temperature_tolerance": F.Constant(15 * P.ppm),
                    "frequency_tolerance": F.Constant(20 * P.ppm),
                },
                pinmap={
                    "1": module.unnamed[0],
                    "2": module.gnd,
                    "3": module.unnamed[1],
                    "4": module.gnd,
                },
            ),
            # PickerOption(
            #    part=LCSC_Part(partno="C258965"),
            #    params={
            #        "frequency": F.Constant(24 * P.Mhertz),
            #        "load_capacitance": F.Constant(12 * P.pF),
            #        "equivalent_series_resistance": F.Constant(50 * P.ohm),
            #        "shunt_capacitance": F.Constant(7 * P.pF),
            #        "frequency_temperature_tolerance": F.Constant(30 * P.ppm),  # 20?
            #        "frequency_tolerance": F.Constant(10 * P.ppm),
            #    },
            #    pinmap={
            #        "1": module.unnamed[0],
            #        "2": module.gnd,
            #        "3": module.unnamed[1],
            #        "4": module.gnd,
            #    },
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C70590"),
            #    params={
            #        "frequency": F.Constant(24 * P.Mhertz),
            #        "load_capacitance": F.Constant(12 * P.pF),
            #        "equivalent_series_resistance": F.Constant(50 * P.ohm),
            #        "shunt_capacitance": F.Constant(3 * P.pF),
            #        "frequency_temperature_tolerance": F.Constant(20 * P.ppm),
            #        "frequency_tolerance": F.Constant(10 * P.ppm),
            #    },
            #    pinmap={
            #        "1": module.unnamed[0],
            #        "2": module.gnd,
            #        "3": module.unnamed[1],
            #        "4": module.gnd,
            #    },
            # ),
        ],
    )


def pick_tvs(module: F.TVS):
    pick_module_by_params(
        module,
        [
            PickerOption(
                # SD03C
                part=LCSC_Part(partno="C907859"),
                params={
                    "reverse_working_voltage": F.Constant(3.3 * P.V),
                    "reverse_leakage_current": F.Constant(200 * P.nA),
                    "reverse_breakdown_voltage": F.Range(4 * P.V, 6 * P.V),
                    "clamping_voltage": F.Constant(9 * P.V),
                    "max_current": F.Constant(38 * P.A),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            PickerOption(
                # SD05C
                part=LCSC_Part(partno="C2687123"),
                params={
                    "reverse_working_voltage": F.Constant(5 * P.V),
                    "reverse_leakage_current": F.Constant(10 * P.uA),
                    "reverse_breakdown_voltage": F.Constant(6 * P.V),
                    "clamping_voltage": F.Constant(9.8 * P.V),
                    "max_current": F.Constant(8 * P.A),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
        ],
    )


def pick_eeprom(module: F.EEPROM):
    pick_module_by_params(
        module,
        [
            PickerOption(
                # TODO: make this a parameter ?
                # part=LCSC_Part(partno="C146734"), # TSSOP-8
                # part=LCSC_Part(partno="C79987"), # SOIC-8
                part=LCSC_Part(partno="C233771"),  # UDFN-8(2x3)
                pinmap={
                    "1": module.address[0].signal,
                    "2": module.address[1].signal,
                    "3": module.address[2].signal,
                    "4": module.power.lv,
                    "5": module.i2c.sda.signal,
                    "6": module.i2c.scl.signal,
                    "7": module.write_protect.signal,
                    "8": module.power.hv,
                },
            )
        ],
    )


def pick_cbm9002A(module: F.CBM9002A_56ILG):
    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C476253"),
                pinmap={
                    "1": module.rdy[0].signal,
                    "2": module.rdy[1].signal,
                    #
                    "4": module.xtalout,
                    "5": module.xtalin,
                    "13": module.ifclk.signal,
                    "54": module.clkout.signal,
                    #
                    "8": module.usb.usb_if.d.p,
                    "9": module.usb.usb_if.d.n,
                    #
                    "15": module.i2c.scl.signal,
                    "16": module.i2c.sda.signal,
                    #
                    "29": module.ctl[0].signal,
                    "30": module.ctl[1].signal,
                    "31": module.ctl[2].signal,
                    #
                    "42": module.reset.signal,
                    #
                    "44": module.wakeup.signal,
                    #
                    "3": module.avcc.hv,
                    "7": module.avcc.hv,
                    #
                    "6": module.avcc.lv,
                    "10": module.avcc.lv,
                    #
                    "11": module.vcc.hv,
                    "17": module.vcc.hv,
                    "27": module.vcc.hv,
                    "32": module.vcc.hv,
                    "43": module.vcc.hv,
                    "55": module.vcc.hv,
                    #
                    "12": module.vcc.lv,
                    "14": module.vcc.lv,  # reserved
                    "26": module.vcc.lv,
                    "28": module.vcc.lv,
                    "41": module.vcc.lv,
                    "53": module.vcc.lv,
                    "56": module.vcc.lv,
                    "57": module.vcc.lv,  # thermal pad
                    #
                    "33": module.PA[0].signal,
                    "34": module.PA[1].signal,
                    "35": module.PA[2].signal,
                    "36": module.PA[3].signal,
                    "37": module.PA[4].signal,
                    "38": module.PA[5].signal,
                    "39": module.PA[6].signal,
                    "40": module.PA[7].signal,
                    #
                    "18": module.PB[0].signal,
                    "19": module.PB[1].signal,
                    "20": module.PB[2].signal,
                    "21": module.PB[3].signal,
                    "22": module.PB[4].signal,
                    "23": module.PB[5].signal,
                    "24": module.PB[6].signal,
                    "25": module.PB[7].signal,
                    #
                    "45": module.PD[0].signal,
                    "46": module.PD[1].signal,
                    "47": module.PD[2].signal,
                    "48": module.PD[3].signal,
                    "49": module.PD[4].signal,
                    "50": module.PD[5].signal,
                    "51": module.PD[6].signal,
                    "52": module.PD[7].signal,
                },
            )
        ],
    )


def pick_ldo(module: F.LDO):
    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C236655"),
                pinmap={
                    "1": module.power_in.lv,
                    "2": module.power_out.hv,
                    "3": module.power_in.hv,
                },
            )
        ],
    )


def pick_sn74lvc541a(module: F.SNx4LVC541A):
    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C113281"),
                # params={
                #    "output_voltage": F.Constant(3.3),
                #    "input_voltage_range": F.Range(3.5, 6.0),
                #    "output_current_max": F.Constant(350e-3),
                # },
                pinmap={
                    "10": module.power.lv,
                    "20": module.power.hv,
                    "1": module.OE[0].signal,
                    "19": module.OE[1].signal,
                    "2": module.A[0].signal,
                    "3": module.A[1].signal,
                    "4": module.A[2].signal,
                    "5": module.A[3].signal,
                    "6": module.A[4].signal,
                    "7": module.A[5].signal,
                    "8": module.A[6].signal,
                    "9": module.A[7].signal,
                    "18": module.Y[0].signal,
                    "17": module.Y[1].signal,
                    "16": module.Y[2].signal,
                    "15": module.Y[3].signal,
                    "14": module.Y[4].signal,
                    "13": module.Y[5].signal,
                    "12": module.Y[6].signal,
                    "11": module.Y[7].signal,
                },
            )
        ],
    )


def pick_resistor_array(module: ResistorArray):
    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C162977"),
                params={"resistance": F.Constant(100 * P.kohm)},
                pinmap={
                    "1": module.resistor[0].unnamed[0],
                    "2": module.resistor[1].unnamed[0],
                    "3": module.resistor[2].unnamed[0],
                    "4": module.resistor[3].unnamed[0],
                    "5": module.resistor[3].unnamed[1],
                    "6": module.resistor[2].unnamed[1],
                    "7": module.resistor[1].unnamed[1],
                    "8": module.resistor[0].unnamed[1],
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C270393"),
                params={"resistance": F.Constant(100 * P.ohm)},
                pinmap={
                    "1": module.resistor[0].unnamed[0],
                    "2": module.resistor[1].unnamed[0],
                    "3": module.resistor[2].unnamed[0],
                    "4": module.resistor[3].unnamed[0],
                    "5": module.resistor[3].unnamed[1],
                    "6": module.resistor[2].unnamed[1],
                    "7": module.resistor[1].unnamed[1],
                    "8": module.resistor[0].unnamed[1],
                },
            ),
        ],
    )


def pick_no_footprint(module: Module):
    module.add_trait(has_part_picked_remove())


def pick_manual_footprint(module: Module):
    module.add_trait(has_part_picked_remove())


# ----------------------------------------------------------


def add_app_pickers(module: Module):
    lookup = {
        F.Resistor: pick_resistor,
        ResistorArray: pick_resistor_array,
        F.LED: pick_led,
        F.LDO: pick_ldo,
        F.SNx4LVC541A: pick_sn74lvc541a,
        F.CBM9002A_56ILG: pick_cbm9002A,
        F.EEPROM: pick_eeprom,
        F.TVS: pick_tvs,
        # F.Diode: pick_diode,
        F.Crystal: pick_crystal,
        F.Capacitor: pick_capacitor,
        SFPEdgeConnector: pick_manual_footprint,
        MountingSlot: pick_manual_footprint,
        F.GenericBusProtection: pick_no_footprint,
        faebrykLogo: pick_manual_footprint,
    }
    F.has_multi_picker.add_pickers_by_type(
        module,
        lookup,
        F.has_multi_picker.FunctionPicker,
    )
