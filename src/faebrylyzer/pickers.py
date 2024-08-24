# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.core import Module
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
            # PickerOption(
            #    part=LCSC_Part(partno="C2286"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.GREEN),
            #        "max_brightness": F.Constant(285e-3),
            #        "forward_voltage": F.Constant(3.7),
            #        "max_current": F.Constant(100e-3),
            #    },
            #    pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C72041"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.BLUE),
            #        "max_brightness": F.Constant(28.5e-3),
            #        "forward_voltage": F.Constant(3.1),
            #        "max_current": F.Constant(100e-3),
            #    },
            #    pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C2290"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.WHITE),
            #        "max_brightness": F.Constant(520e-3),
            #        "forward_voltage": F.Constant(3.1),
            #        "max_current": F.Constant(60e-3),
            #    },
            #    pinmap={"2": module.IFs.cathode, "1": module.IFs.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C2296"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.YELLOW),
            #        "max_brightness": F.Constant(113e-3),
            #        "forward_voltage": F.Constant(2.1),
            #        "max_current": F.Constant(20e-3),
            #    },
            #    pinmap={"2": module.IFs.cathode, "1": module.IFs.anode},
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
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
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
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
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
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
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
            #    pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
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
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
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
            #    pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
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
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
            ),
            # XL-1606UWC
            PickerOption(
                part=LCSC_Part(partno="C965866"),
                params={
                    "color": F.Constant(
                        F.LED.Color.WHARM_WHITE
                        # TypicalColorByTemperature.WARM_WHITE_FLUORESCENT_LED
                    ),
                    "max_brightness": F.Constant(1100 * P.millicandela),
                    "forward_voltage": F.Constant(3.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
            ),
        ],
    )


def pick_header(module: F.Header):
    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C2691448"),
                params={
                    "horizontal_pin_count": F.Constant(1),
                    "vertical_pin_count": F.Constant(4),
                    # "pin_pitch": F.Constant(2.54),
                    # "pin_type": F.Constant(F.Header.PinType.MALE),
                    # "pad_type": F.Constant(F.Header.PadType.THROUGH_HOLE),
                    # "angle": F.Constant(F.Header.Angle.STRAIGHT),
                },
                pinmap={f"{i+1}": module.IFs.unnamed[i] for i in range(4)},
            ),
            # PickerOption(
            #    part=LCSC_Part(partno="C492421"),
            #    params={
            #        "horizontal_pin_count": F.Constant(2),
            #        "vertical_pin_count": F.Constant(4),
            #        "pin_pitch": F.Constant(2.54),
            #        "pin_type": F.Constant(F.Header.PinType.MALE),
            #        "pad_type": F.Constant(F.Header.PadType.THROUGH_HOLE),
            #        "angle": F.Constant(F.Header.Angle.STRAIGHT),
            #    },
            #    pinmap={f"{i+1}": module.IFs.unnamed[i] for i in range(8)},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C7501276"),
            #    params={
            #        "horizontal_pin_count": F.Constant(2),
            #        "vertical_pin_count": F.Constant(5),
            #        "pin_pitch": F.Constant(2.54),
            #        "pin_type": F.Constant(F.Header.PinType.MALE),
            #        "pad_type": F.Constant(F.Header.PadType.THROUGH_HOLE),
            #        "angle": F.Constant(F.Header.Angle.STRAIGHT),
            #    },
            #    pinmap={f"{i+1}": module.IFs.unnamed[i] for i in range(10)},
            # ),
            PickerOption(
                part=LCSC_Part(partno="C225521"),
                params={
                    "horizontal_pin_count": F.Constant(2),
                    "vertical_pin_count": F.Constant(6),
                    # "pin_pitch": F.Constant(2.54),
                    # "pin_type": F.Constant(F.Header.PinType.MALE),
                    # "pad_type": F.Constant(F.Header.PadType.THROUGH_HOLE),
                    # "angle": F.Constant(F.Header.Angle.STRAIGHT),
                },
                pinmap={
                    f"{i+1}": module.IFs.unnamed[i] for i in range(4)
                },  # TODO: range(12)
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
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
            )
        ],
    )


def pick_crystal(module: F.Crystal):
    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C258965"),
                params={
                    "frequency": F.Constant(24 * P.Mhertz),
                    "load_impedance": F.Constant(12 * P.pF),
                    "equivalent_series_resistance": F.Constant(50 * P.ohm),
                    "shunt_capacitance": F.Constant(7 * P.pF),
                    "frequency_temperature_tolerance": F.Constant(30 * P.ppm),  # 20?
                    "frequency_tolerance": F.Constant(10 * P.ppm),
                },
                pinmap={
                    "1": module.IFs.unnamed[0],
                    "2": module.IFs.gnd,
                    "3": module.IFs.unnamed[1],
                    "4": module.IFs.gnd,
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C70590"),
                params={
                    "frequency": F.Constant(24 * P.Mhertz),
                    "load_impedance": F.Constant(12 * P.pF),
                    "equivalent_series_resistance": F.Constant(50 * P.ohm),
                    "shunt_capacitance": F.Constant(3 * P.pF),
                    "frequency_temperature_tolerance": F.Constant(20 * P.ppm),
                    "frequency_tolerance": F.Constant(10 * P.ppm),
                },
                pinmap={
                    "1": module.IFs.unnamed[0],
                    "2": module.IFs.gnd,
                    "3": module.IFs.unnamed[1],
                    "4": module.IFs.gnd,
                },
            ),
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
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
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
                pinmap={"1": module.IFs.cathode, "2": module.IFs.anode},
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
                    "1": module.IFs.address[0].IFs.signal,
                    "2": module.IFs.address[1].IFs.signal,
                    "3": module.IFs.address[2].IFs.signal,
                    "4": module.IFs.power.IFs.lv,
                    "5": module.IFs.i2c.IFs.sda.IFs.signal,
                    "6": module.IFs.i2c.IFs.scl.IFs.signal,
                    "7": module.IFs.write_protect.IFs.signal,
                    "8": module.IFs.power.IFs.hv,
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
                    "1": module.IFs.rdy[0].IFs.signal,
                    "2": module.IFs.rdy[1].IFs.signal,
                    #
                    "4": module.IFs.xtalout,
                    "5": module.IFs.xtalin,
                    "13": module.IFs.ifclk.IFs.signal,
                    "54": module.IFs.clkout.IFs.signal,
                    #
                    "8": module.IFs.usb.IFs.usb_if.IFs.d.IFs.p,
                    "9": module.IFs.usb.IFs.usb_if.IFs.d.IFs.n,
                    #
                    "15": module.IFs.i2c.IFs.scl.IFs.signal,
                    "16": module.IFs.i2c.IFs.sda.IFs.signal,
                    #
                    "29": module.IFs.ctl[0].IFs.signal,
                    "30": module.IFs.ctl[1].IFs.signal,
                    "31": module.IFs.ctl[2].IFs.signal,
                    #
                    "42": module.IFs.reset.IFs.signal,
                    #
                    "44": module.IFs.wakeup.IFs.signal,
                    #
                    "3": module.IFs.avcc.IFs.hv,
                    "7": module.IFs.avcc.IFs.hv,
                    #
                    "6": module.IFs.avcc.IFs.lv,
                    "10": module.IFs.avcc.IFs.lv,
                    #
                    "11": module.IFs.vcc.IFs.hv,
                    "17": module.IFs.vcc.IFs.hv,
                    "27": module.IFs.vcc.IFs.hv,
                    "32": module.IFs.vcc.IFs.hv,
                    "43": module.IFs.vcc.IFs.hv,
                    "55": module.IFs.vcc.IFs.hv,
                    #
                    "12": module.IFs.vcc.IFs.lv,
                    "14": module.IFs.vcc.IFs.lv,  # reserved
                    "26": module.IFs.vcc.IFs.lv,
                    "28": module.IFs.vcc.IFs.lv,
                    "41": module.IFs.vcc.IFs.lv,
                    "53": module.IFs.vcc.IFs.lv,
                    "56": module.IFs.vcc.IFs.lv,
                    "57": module.IFs.vcc.IFs.lv,  # thermal pad
                    #
                    "33": module.IFs.PA[0].IFs.signal,
                    "34": module.IFs.PA[1].IFs.signal,
                    "35": module.IFs.PA[2].IFs.signal,
                    "36": module.IFs.PA[3].IFs.signal,
                    "37": module.IFs.PA[4].IFs.signal,
                    "38": module.IFs.PA[5].IFs.signal,
                    "39": module.IFs.PA[6].IFs.signal,
                    "40": module.IFs.PA[7].IFs.signal,
                    #
                    "18": module.IFs.PB[0].IFs.signal,
                    "19": module.IFs.PB[1].IFs.signal,
                    "20": module.IFs.PB[2].IFs.signal,
                    "21": module.IFs.PB[3].IFs.signal,
                    "22": module.IFs.PB[4].IFs.signal,
                    "23": module.IFs.PB[5].IFs.signal,
                    "24": module.IFs.PB[6].IFs.signal,
                    "25": module.IFs.PB[7].IFs.signal,
                    #
                    "45": module.IFs.PD[0].IFs.signal,
                    "46": module.IFs.PD[1].IFs.signal,
                    "47": module.IFs.PD[2].IFs.signal,
                    "48": module.IFs.PD[3].IFs.signal,
                    "49": module.IFs.PD[4].IFs.signal,
                    "50": module.IFs.PD[5].IFs.signal,
                    "51": module.IFs.PD[6].IFs.signal,
                    "52": module.IFs.PD[7].IFs.signal,
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
                    "1": module.IFs.power_in.IFs.lv,
                    "2": module.IFs.power_out.IFs.hv,
                    "3": module.IFs.power_in.IFs.hv,
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
                    "10": module.IFs.vcc.IFs.lv,
                    "20": module.IFs.vcc.IFs.hv,
                    "1": module.IFs.OE[0].IFs.signal,
                    "19": module.IFs.OE[1].IFs.signal,
                    "2": module.IFs.A[0].IFs.signal,
                    "3": module.IFs.A[1].IFs.signal,
                    "4": module.IFs.A[2].IFs.signal,
                    "5": module.IFs.A[3].IFs.signal,
                    "6": module.IFs.A[4].IFs.signal,
                    "7": module.IFs.A[5].IFs.signal,
                    "8": module.IFs.A[6].IFs.signal,
                    "9": module.IFs.A[7].IFs.signal,
                    "18": module.IFs.Y[0].IFs.signal,
                    "17": module.IFs.Y[1].IFs.signal,
                    "16": module.IFs.Y[2].IFs.signal,
                    "15": module.IFs.Y[3].IFs.signal,
                    "14": module.IFs.Y[4].IFs.signal,
                    "13": module.IFs.Y[5].IFs.signal,
                    "12": module.IFs.Y[6].IFs.signal,
                    "11": module.IFs.Y[7].IFs.signal,
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
                    "1": module.NODEs.resistor[0].IFs.unnamed[0],
                    "2": module.NODEs.resistor[1].IFs.unnamed[0],
                    "3": module.NODEs.resistor[2].IFs.unnamed[0],
                    "4": module.NODEs.resistor[3].IFs.unnamed[0],
                    "5": module.NODEs.resistor[3].IFs.unnamed[1],
                    "6": module.NODEs.resistor[2].IFs.unnamed[1],
                    "7": module.NODEs.resistor[1].IFs.unnamed[1],
                    "8": module.NODEs.resistor[0].IFs.unnamed[1],
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C270393"),
                params={"resistance": F.Constant(100 * P.ohm)},
                pinmap={
                    "1": module.NODEs.resistor[0].IFs.unnamed[0],
                    "2": module.NODEs.resistor[1].IFs.unnamed[0],
                    "3": module.NODEs.resistor[2].IFs.unnamed[0],
                    "4": module.NODEs.resistor[3].IFs.unnamed[0],
                    "5": module.NODEs.resistor[3].IFs.unnamed[1],
                    "6": module.NODEs.resistor[2].IFs.unnamed[1],
                    "7": module.NODEs.resistor[1].IFs.unnamed[1],
                    "8": module.NODEs.resistor[0].IFs.unnamed[1],
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
        F.Header: pick_header,
        # F.Header: pick_header,
        F.LDO: pick_ldo,
        F.SNx4LVC541A: pick_sn74lvc541a,
        F.CBM9002A_56ILG: pick_cbm9002A,
        F.EEPROM: pick_eeprom,
        F.TVS: pick_tvs,
        F.Diode: pick_diode,
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
