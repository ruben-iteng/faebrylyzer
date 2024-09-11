# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging
import subprocess

import faebryk.library._F as F
from faebryk.exporters.pcb.kicad.transformer import Font, PCB_Transformer
from faebryk.exporters.pcb.layout.absolute import LayoutAbsolute
from faebryk.exporters.pcb.layout.extrude import LayoutExtrude
from faebryk.exporters.pcb.layout.matrix import LayoutMatrix
from faebryk.exporters.pcb.layout.typehierarchy import LayoutTypeHierarchy
from faebryk.libs.geometry.basic import Geometry
from faebryk.libs.kicad.fileformats import (
    C_effects,
    C_wh,
    C_xy,
    C_xyr,
)

from faebrylyzer.app import faebrylyzerApp
from faebrylyzer.library.faebrykLogo import faebrykLogo
from faebrylyzer.library.faebrylyzerModule import faebrylyzerModule
from faebrylyzer.library.ResistorArray import ResistorArray

Point2D = Geometry.Point2D

logger = logging.getLogger(__name__)


# ----------------------------------------
#               Functions
# ----------------------------------------
def apply_routing(transformer: PCB_Transformer):
    pass


def apply_root_layout(app: faebrylyzerApp, board_size: tuple[float, float]):
    Point = F.has_pcb_position.Point
    L = F.has_pcb_position.layer_type
    LVL = LayoutTypeHierarchy.Level

    board_width, board_height = board_size

    # manual placement
    layouts = [
        LVL(
            mod_type=faebrykLogo,
            layout=LayoutAbsolute(Point((20, 0, 0, L.TOP_LAYER))),
        ),
        LVL(
            mod_type=faebrylyzerModule,
            layout=LayoutAbsolute(Point((0, 0, 90, L.TOP_LAYER))),
        ),
        LVL(
            mod_type=F.PoweredLED,
            layout=LayoutExtrude(
                base=Point((3.5, -6.75, 0, L.BOTTOM_LAYER)),
                vector=(0, 4.5, 0),
            ),
            children_layout=LayoutTypeHierarchy(
                layouts=[
                    LVL(
                        mod_type=F.LED,
                        layout=LayoutAbsolute(Point((0, 0, 0, L.NONE))),
                    ),
                    LVL(
                        mod_type=F.Resistor,
                        layout=LayoutAbsolute(Point((4.4, 0, 0, L.NONE))),
                    ),
                ]
            ),
        ),
        LVL(
            mod_type=F.CBM9002A_56ILG_Reference_Design,
            layout=LayoutAbsolute(Point((18, 0, 0, L.BOTTOM_LAYER))),
            children_layout=LayoutTypeHierarchy(
                layouts=[
                    LVL(
                        mod_type=F.CBM9002A_56ILG,
                        layout=LayoutAbsolute(Point((0, 0, 0, L.NONE))),
                        children_layout=LayoutTypeHierarchy(
                            layouts=[
                                LVL(
                                    mod_type=F.Capacitor,
                                    layout=LayoutExtrude(
                                        base=Point((-5.5, 2.25, 90, L.NONE)),
                                        vector=(4.5, 0, 180),
                                        dynamic_rotation=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    LVL(
                        mod_type=F.Diode,
                        layout=LayoutAbsolute(Point((-0.5, 5.75, 180, L.NONE))),
                    ),
                    LVL(
                        mod_type=F.Resistor,
                        layout=LayoutAbsolute(Point((-3.25, 5.75, 0, L.NONE))),
                    ),
                    LVL(
                        mod_type=F.Crystal_Oscillator,
                        layout=LayoutAbsolute(Point((-1.5, -7, 180, L.NONE))),
                        children_layout=LayoutTypeHierarchy(
                            layouts=[
                                LVL(
                                    mod_type=F.Crystal,
                                    layout=LayoutAbsolute(Point((0, 0, 0, L.NONE))),
                                ),
                                LVL(
                                    mod_type=F.Capacitor,
                                    layout=LayoutExtrude(
                                        base=Point((-2, 0, 270, L.NONE)),
                                        vector=(0, -4, 180),
                                        dynamic_rotation=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                ]
            ),
        ),
        LVL(
            mod_type=F.SNx4LVC541A,
            layout=LayoutAbsolute(Point((30, 0, 270, L.BOTTOM_LAYER))),
            children_layout=LayoutTypeHierarchy(
                layouts=[
                    LVL(
                        mod_type=F.Capacitor,
                        layout=LayoutAbsolute(Point((-4.75, 2, 180, L.NONE))),
                    ),
                ]
            ),
        ),
        LVL(
            mod_type=ResistorArray,
            layout=LayoutMatrix(
                base=Point((24, 1.75, 270, L.TOP_LAYER)),
                vector=(2.75, 12, 0),
                distribution=(2, 3),
            ),
        ),
        LVL(
            mod_type=F.LDO,
            layout=LayoutAbsolute(Point((25, 6.5, 180, L.BOTTOM_LAYER))),
            children_layout=LayoutTypeHierarchy(
                layouts=[
                    LVL(
                        mod_type=F.Capacitor,
                        layout=LayoutExtrude(
                            base=Point((-3, 0, 0, L.NONE)),
                            vector=(6, 0, 90),
                        ),
                    ),
                    LVL(
                        mod_type=F.Diode,
                        layout=LayoutExtrude(
                            base=Point((-8.5, 2, 0, L.NONE)),
                            vector=(0, 9, 0),
                            reverse_order=True,
                        ),
                    ),
                ]
            ),
        ),
        LVL(
            mod_type=F.EEPROM,
            layout=LayoutAbsolute(Point((24.75, -6, 270, L.BOTTOM_LAYER))),
            children_layout=LayoutTypeHierarchy(
                layouts=[
                    LVL(
                        mod_type=F.Resistor,
                        layout=LayoutExtrude(
                            base=Point((1.5, -1.8, 0, L.NONE)),
                            vector=(0, 3.6, 180),
                            reverse_order=True,
                        ),
                    ),
                    LVL(
                        mod_type=F.Capacitor,
                        layout=LayoutAbsolute(Point((-0.9, 1.8, 180, L.NONE))),
                    ),
                ]
            ),
        ),
    ]

    app.add_trait(F.has_pcb_layout_defined(LayoutTypeHierarchy(layouts)))

    # set coordinate system
    app.add_trait(F.has_pcb_position_defined(Point((0, board_height / 2, 0, L.NONE))))


def add_zone(transformer: PCB_Transformer, outline: list[Point2D], offset: float = 1):
    transformer.insert_zone(
        net=transformer.get_net(F.Net.with_name("gnd")),
        layers=[*transformer.get_copper_layers()],
        polygon=Geometry.rect_to_polygon(
            Geometry.bbox(
                [Geometry.Point2D(coord) for coord in outline],
                offset,
            )
        ),
    )


def add_graphical_elements(
    transformer: PCB_Transformer, board_size: tuple[float, float]
):
    app = transformer.app
    assert isinstance(app, faebrylyzerApp)

    board_width, board_height = board_size

    # project name and version
    board_name = "faebrylyzer"
    char_size = board_height / (len(board_name) - 1)
    transformer.insert_text(
        text=board_name,
        at=C_xyr(36, board_height / 2, 90),
        layer="F.SilkS",
        font=Font(size=C_wh(char_size, char_size), thickness=0.4),
        knockout=True,
    )
    try:
        git_human_version = (
            subprocess.check_output(["git", "describe", "--always"])
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        logger.warning("Cannot get git project version")
        git_human_version = "Cannot get git project version"

    transformer.insert_text(
        text=git_human_version,
        at=C_xyr(33, board_height / 2, 90),
        layer="F.SilkS",
        font=Font(size=C_wh(1, 1), thickness=0.15),
        knockout=True,
    )

    # line to indicate mechanical mounting
    for layer in ["F.SilkS", "B.SilkS"]:
        for y_location in [0, board_height]:
            transformer.insert_line(
                start=C_xy(0, y_location),
                end=C_xy(board_width, y_location),
                width=1,
                layer=layer,
            )

    # LED text
    led_text_offset_x = 1.25
    led_base_y = 2
    led_spacing_y = 4.5
    led_font = Font(size=C_wh(2, 2), thickness=0.25)
    for i, cled in enumerate(app.channel_leds):
        # TODO: does not work, nodes get a position way later (see main.py)
        # (x, y, r, layer) = cled.led.get_trait(F.F.has_pcb_position).get_position()
        transformer.insert_text(
            text=f"[ ] CH{i+1}",
            at=C_xyr(led_text_offset_x, led_base_y + led_spacing_y * i, 0),
            layer="F.SilkS",
            font=led_font,
            knockout=True,
            alignment=(
                C_effects.E_justify.left,
                C_effects.E_justify.center,
                C_effects.E_justify.normal,
            ),
        )
    transformer.insert_text(
        text="[ ] PWR",
        at=C_xyr(led_text_offset_x, led_base_y + led_spacing_y * 2, 0),
        layer="F.SilkS",
        font=led_font,
        knockout=True,
        alignment=(
            C_effects.E_justify.left,
            C_effects.E_justify.center,
            C_effects.E_justify.normal,
        ),
    )
    transformer.insert_text(
        text="[ ] STATUS",
        at=C_xyr(led_text_offset_x, led_base_y + led_spacing_y * 3, 0),
        layer="F.SilkS",
        font=led_font,
        knockout=True,
        alignment=(
            C_effects.E_justify.left,
            C_effects.E_justify.center,
            C_effects.E_justify.normal,
        ),
    )

    transformer.insert_jlcpcb_qr(
        size=PCB_Transformer.JLCPBC_QR_Size.SMALL_5x5mm,
        center_at=C_xy(28.5, board_height / 2),
        layer="F.SilkS",
        number=True,
    )

    # move all reference designators to the same position
    transformer.set_designator_position(
        offset=0.75,
        displacement=C_xy(0, 0),
        offset_side=PCB_Transformer.Side.BOTTOM,
        layer=None,
        font=Font(size=C_wh(0.5, 0.5), thickness=0.1),
        knockout=None,
    )


def transform_pcb(transformer: PCB_Transformer):
    app = transformer.app
    assert isinstance(app, faebrylyzerApp)

    # ----------------------------------------
    #               PCB outline
    # ----------------------------------------
    board_width = 45
    board_height = 18
    outline_coordinates = [
        (0, 0),
        (board_width, 0),
        (board_width, 3),
        (board_width - 6.5, 3),
        # (board_width - 6.5, 0),
        (board_width - 6.5, 4.6),
        (board_width, 4.6),
        (board_width, board_height / 2 + 4.6),
        (board_width - 6.5, board_height / 2 + 4.6),
        # (board_width - 6.5, board_height),
        (board_width - 6.5, board_height - 3),
        (board_width, board_height - 3),
        (board_width, board_height),
        (0, board_height),
    ]
    # TODO reenable
    # transformer.insert_pcb_outline(
    #    outline_coordinates,
    #    corner_radius_mm=0.5,
    # )

    # ----------------------------------------
    #               Copper zones
    # ----------------------------------------
    add_zone(transformer, outline_coordinates, offset=1)

    # ----------------------------------------
    #               Vias
    # ----------------------------------------
    # transformer.insert_via(
    #    coord=(0, 0),
    #    net=transformer.get_net(F.Net.with_name("gnd")),
    #    size_drill=(0.3, 0),
    # )

    # ----------------------------------------
    #               Layout
    # ----------------------------------------
    apply_root_layout(app, board_size=(board_width, board_height))

    # ----------------------------------------
    #               Routing
    # ----------------------------------------
    apply_routing(transformer)

    # ----------------------------------------
    #           Graphical elements
    # ----------------------------------------
    add_graphical_elements(transformer, board_size=(board_width, board_height))
