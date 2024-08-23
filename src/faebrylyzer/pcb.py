# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging
import subprocess

import faebryk.library._F as F
from faebryk.core.util import get_node_children_all
from faebryk.exporters.pcb.kicad.transformer import Font, PCB_Transformer
from faebryk.exporters.pcb.layout.absolute import LayoutAbsolute
from faebryk.exporters.pcb.layout.extrude import LayoutExtrude
from faebryk.exporters.pcb.layout.matrix import LayoutMatrix
from faebryk.exporters.pcb.layout.typehierarchy import LayoutTypeHierarchy
from faebryk.library.has_pcb_layout_defined import has_pcb_layout_defined
from faebryk.library.has_pcb_position import has_pcb_position
from faebryk.library.has_pcb_position_defined import has_pcb_position_defined
from faebryk.library.Net import Net
from faebryk.libs.geometry.basic import Geometry
from faebryk.libs.kicad.fileformats import (
    C_effects,
    C_line,
    C_stroke,
    C_text_layer,
    C_wh,
    C_xy,
    C_xyr,
)
from faebrylyzer.app import faebrylyzerApp
from faebrylyzer.library.faebrylyzerModule import faebrylyzerModule
from faebrylyzer.library.ResistorArray import ResistorArray
from pyparsing import C

logger = logging.getLogger(__name__)

"""
Here you can do PCB scripting.
E.g placing components, layer switching, mass renaming, etc.
"""


# ----------------------------------------
#               Functions
# ----------------------------------------
def apply_routing(transformer: PCB_Transformer):
    for node in get_node_children_all(transformer.app):
        # set routing strategy for capacitors to direct line
        if isinstance(node, F.Capacitor):
            node.add_trait(
                F.has_pcb_routing_strategy_greedy_direct_line(
                    F.has_pcb_routing_strategy_greedy_direct_line.Topology.DIRECT
                )
            )


def apply_root_layout(app: faebrylyzerApp, board_size: tuple[float, float]):
    Point = has_pcb_position.Point
    L = has_pcb_position.layer_type
    LVL = LayoutTypeHierarchy.Level

    board_width, board_height = board_size

    # manual placement
    layouts = [
        LVL(
            mod_type=faebrylyzerModule,
            layout=LayoutAbsolute(Point((0, board_height / 2, 90, L.TOP_LAYER))),
        ),
        LVL(
            mod_type=F.Diode,
            layout=LayoutAbsolute(Point((33.5, 5.5, 180, L.BOTTOM_LAYER))),
        ),
        LVL(
            mod_type=F.PoweredLED,
            layout=LayoutExtrude(
                base=Point((3.5, 3.25, 0, L.BOTTOM_LAYER)),
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
            layout=LayoutAbsolute(Point((18, 10, 0, L.BOTTOM_LAYER))),
            children_layout=LayoutTypeHierarchy(
                layouts=[
                    LVL(
                        mod_type=F.CBM9002A_56ILG,
                        layout=LayoutAbsolute(Point((0, 0, 0, L.NONE))),
                        children_layout=LayoutTypeHierarchy(layouts=[]),
                    ),
                    LVL(
                        mod_type=F.Diode,
                        layout=LayoutAbsolute(Point((-0.5, 5.75, 180, L.NONE))),
                        children_layout=LayoutTypeHierarchy(layouts=[]),
                    ),
                    LVL(
                        mod_type=F.Resistor,
                        layout=LayoutAbsolute(Point((-0.5, 7, 0, L.NONE))),
                        children_layout=LayoutTypeHierarchy(layouts=[]),
                    ),
                    LVL(
                        mod_type=F.Crystal_Oscillator,
                        layout=LayoutAbsolute(Point((-1.5, -6.5, 180, L.NONE))),
                        children_layout=LayoutTypeHierarchy(
                            layouts=[
                                LVL(
                                    mod_type=F.Crystal,
                                    layout=LayoutAbsolute(Point((0, 0, 0, L.NONE))),
                                ),
                                LVL(
                                    mod_type=F.Capacitor,
                                    layout=LayoutExtrude(
                                        base=Point((-3, 0, 270, L.NONE)),
                                        vector=(0, -6, 180),
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
            layout=LayoutAbsolute(Point((30, board_height / 2, 270, L.BOTTOM_LAYER))),
            children_layout=LayoutTypeHierarchy(layouts=[]),
        ),
        LVL(
            mod_type=ResistorArray,
            layout=LayoutMatrix(
                base=Point((24, board_height / 2 - 0.75, 270, L.TOP_LAYER)),
                vector=(2.75, 12, 0),
                distribution=(2, 3),
            ),
        ),
        LVL(
            mod_type=F.LDO,
            layout=LayoutAbsolute(Point((25, 16.5, 180, L.BOTTOM_LAYER))),
            children_layout=LayoutTypeHierarchy(layouts=[]),
        ),
        LVL(
            mod_type=F.EEPROM,
            layout=LayoutAbsolute(Point((24.75, 3.5, 270, L.BOTTOM_LAYER))),
            children_layout=LayoutTypeHierarchy(
                layouts=[
                    LVL(
                        mod_type=F.Resistor,
                        layout=LayoutExtrude(
                            base=Point((0.5, -2, 0, L.NONE)),
                            vector=(0, 4, 180),
                            reverse_order=True,
                        ),
                    ),
                ]
            ),
        ),
    ]

    app.add_trait(has_pcb_layout_defined(LayoutTypeHierarchy(layouts)))

    # set coordinate system
    app.add_trait(has_pcb_position_defined(Point((0, 0, 0, L.NONE))))


def set_outline(
    transformer: PCB_Transformer,
    outline_coordinates: list,
    outline_corner_radius_mm: float = 0.0,
):
    # create line objects from coordinates
    outline_lines = []
    for coordinate in outline_coordinates:
        outline_lines.append(
            C_line(
                start=C_xy(coordinate[0], coordinate[1]),
                end=C_xy(
                    outline_coordinates[
                        (outline_coordinates.index(coordinate) + 1)
                        % len(outline_coordinates)
                    ][0],
                    outline_coordinates[
                        (outline_coordinates.index(coordinate) + 1)
                        % len(outline_coordinates)
                    ][1],
                ),
                stroke=C_stroke(0.05, C_stroke.E_type.solid),
                layer="Edge.Cuts",
                uuid=transformer.gen_uuid(mark=True),
            )
        )
    transformer.set_pcb_outline_complex(
        outline_lines,
        remove_existing_outline=True,
        corner_radius_mm=outline_corner_radius_mm,
    )


def add_zones(transformer: PCB_Transformer, outline: list, offset: float = 1):
    # for _layer in transformer.get_copper_layers():
    transformer.insert_zone(
        net=transformer.get_net(Net.with_name("gnd")),
        layers=["F.Cu", "B.Cu", "In1.Cu", "In2.Cu"],
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
    transformer.insert_text(
        text="faebrylyzer",
        at=C_xyr(36, board_height / 2, 90),
        front=True,
        font=Font(size=C_wh(2.4, 2.4), thickness=0.4),
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
        front=True,
        font=Font(size=C_wh(1, 1), thickness=0.15),
        knockout=True,
    )

    # LED text
    for i, cled in enumerate(app.NODEs.channel_leds):
        # (x, y, r, layer) = cled.NODEs.led.get_trait(F.has_pcb_position).get_position()
        led_text_offset_x = 1.25
        led_base_y = 3.25
        led_spacing_y = 4.5
        led_font = Font(size=C_wh(2, 2), thickness=0.25)
        transformer.insert_text(
            text=f"[ ] CH{i+1}",
            at=C_xyr(led_text_offset_x, led_base_y + led_spacing_y * i, 0),
            front=True,
            font=led_font,
            knockout=True,
            alignment_vertical=C_effects.E_justify.left,
        )

    transformer.insert_text(
        text="[ ] 5V",
        at=C_xyr(led_text_offset_x, led_base_y + led_spacing_y * 2, 0),
        front=True,
        font=led_font,
        knockout=True,
        alignment_vertical=C_effects.E_justify.left,
    )

    transformer.insert_text(
        text="[ ] STATUS",
        at=C_xyr(led_text_offset_x, led_base_y + led_spacing_y * 3, 0),
        front=True,
        font=led_font,
        knockout=True,
        alignment_vertical=C_effects.E_justify.left,
    )

    # move all reference designators to the same position
    footprints = [
        cmp.get_trait(PCB_Transformer.has_linked_kicad_footprint).get_fp()
        for cmp in get_node_children_all(transformer.app)
        if cmp.has_trait(PCB_Transformer.has_linked_kicad_footprint)
    ]
    for f in footprints:
        ref = f.propertys["Reference"]
        ref.layer = C_text_layer("F.SilkS" if f.layer.startswith("F") else "B.SilkS")
        ref.effects.font = Font(size=C_wh(0.5, 0.5), thickness=0.1)


def transform_pcb(transformer: PCB_Transformer):
    app = transformer.app
    assert isinstance(app, faebrylyzerApp)

    # ----------------------------------------
    #               PCB outline
    # ----------------------------------------
    board_width = 45
    board_height = 20
    outline = [
        (0, 0),
        (board_width - 6.5, 0),
        (board_width - 6.5, 5.4),
        (board_width, 5.4),
        (board_width, board_height - 5.4),
        (board_width - 6.5, board_height - 5.4),
        (board_width - 6.5, board_height),
        (0, board_height),
    ]
    set_outline(transformer, outline, outline_corner_radius_mm=0)

    # ----------------------------------------
    #               Copper zones
    # ----------------------------------------
    add_zones(transformer, outline, offset=1)

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
