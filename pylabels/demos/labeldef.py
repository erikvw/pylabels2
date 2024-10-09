# This file is part of pylabels, a Python library to create PDFs for printing
# labels.
# Copyright (C) 2012, 2013, 2014 Blair Bonnett
#
# pylabels is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pylabels is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pylabels.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import annotations

import json
from pathlib import Path

from pylabels.specifications import Specification

# just some simple static constants
I2MM = 25.4
SHEET_SIZES = {"letter": (8.5, 11), "A4": (210, 297), "A5": (148, 210)}


def build_label_def(json_file_path: Path | str) -> dict:
    """The basic purpose of this method is to load the JSON file
    specs and turn it into a dictionary of dictionaries where the
    label name is the key.

    The dictionary that is the value should then contain all the
    necessary parameters to build a specification.

    :param json_file_path:
    :return: a dictionary of label specs
    """

    json_file_path = Path(json_file_path)

    with json_file_path.open() as json_file:
        json_data = json.load(json_file)
        d = {}
        for label in json_data["label"]:
            d[label["name"]] = label
        return d


def build_spec(label_name: str, spec_dictionary: dict) -> Specification:
    """
    Buld a specification from the dictionary we parsed in build_label_def
    :param label_name: the label name
    :param spec_dictionary: the dictionary of labels
    :return: a specification
    """
    data = spec_dictionary[label_name]
    # this gets the multiplier, if it is defined in inches
    # we multiply to get everything into mm
    mult = I2MM if data.pop("measurement") == "in" else 1
    data.pop("name")
    # let's get the defaults out of the dictionary explicitly
    page_size = SHEET_SIZES[data.pop("page_size")]
    sheet_width = page_size[0] * mult
    sheet_height = page_size[1] * mult
    columns = data.pop("columns")
    rows = data.pop("rows")
    label_width = data.pop("label_width") * mult
    label_height = data.pop("label_height") * mult
    # now that we have popped all the required stuff out of the dictionary
    # we can just use defaults for the rest of the stuff
    # here is a list of things that dont get multiplied by the mulitplier
    non_mult = ["corner_radius", "padding_radius", "background_image", "background_filename"]
    # holder for the transformed optional stuff
    opt_data = {}
    for k in data.keys():
        if k in non_mult or not (isinstance(data[k], (int, float))):
            opt_data[k] = data[k]
        else:
            opt_data[k] = data[k] * mult
    spec = Specification(
        sheet_width=sheet_width,
        sheet_height=sheet_height,
        columns=columns,
        rows=rows,
        label_height=label_height,
        label_width=label_width,
        **opt_data,
    )
    return spec
