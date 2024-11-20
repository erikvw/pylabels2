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

from pathlib import Path

from reportlab.graphics import shapes
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

from pylabels import Sheet
from pylabels.demos.labeldef import build_label_def, build_spec

# Everything in pylabels is in mm, but for row heights we need points
MM2P = 2.83465

# Get the path to the demos directory.
base_path = Path(__file__).parent

# get the label definations
label_defs = build_label_def(base_path / "labeldef.json")

# get our spec
spec = build_spec("Avery 5160", label_defs)


# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the name to put on the tag.
def write_address(label, width, height, address) -> None:
    # first split the address into lines, this is for calculating the
    # length of the longest line
    address_lines = address.split("\n")
    # get the info
    number_lines, line_length = string_size(address)
    # find the longest string line
    longest_line = address_lines[line_length.index(max(line_length))]
    font_size = 12
    text_width = width - 10
    text_height = height - 10
    line_height = (font_size / MM2P) * 1.5
    # make sure it fits on a label
    longest_width = stringWidth(longest_line, "Times-Roman", font_size)
    total_height = number_lines * line_height
    while (longest_width > text_width) or (total_height > text_height):
        font_size *= 0.9
        longest_width = stringWidth(longest_line, "Times-Roman", font_size)
        line_height = (font_size / MM2P) * 1.5
        total_height = number_lines * line_height
    # now the font is correct, we need to specify the position of the string
    # the horizontal part is easy
    h_location = width / 2
    # now for this algo we are going to define the center as zero to make things easy
    # this is no big deal as we can always add the constant to the vector
    # first we need to determine if there are an odd or even number of lines
    vertical_lines = []
    if number_lines % 2 == 0:
        # if its even, simply take put n/2 above the center and n/2 below
        _l = number_lines // 2
        for i in range(_l):
            if i == 0:
                vertical_lines.append((i + 1) * (line_height * 0.90))
                vertical_lines.append((i + 1) * (-line_height * 0.90))
            else:
                vertical_lines.append(((i + 1) * (line_height)) + (line_height * 0.65))
                vertical_lines.append(((i + 1) * (-line_height)) - (line_height * 0.65))
    else:
        # odd is a little tricker as the first line gets placed at 0
        # but then we need to move from 1/2 the line height up and down
        _l = number_lines // 2
        vertical_lines.append(0)
        _s = line_height / 2.0
        for i in range(_l):
            _pu = ((i + 1) * -line_height) - _s
            _pp = ((i + 1) * line_height) + _s
            vertical_lines.append(_pu)
            vertical_lines.append(_pp)
    # ok now we have a list with the zero based line height positions
    # we can simply sort them, and add the scalar
    vertical_lines.sort(reverse=True)
    vertical_pos = [x + height / 2 for x in vertical_lines]
    # after all that, we can finally write the label
    for c, line in enumerate(address_lines):
        s = shapes.String(h_location, vertical_pos[c], line, textAnchor="middle")
        s.fontName = "Times-Roman"
        s.fontSize = font_size
        s.fillColor = colors.black
        label.add(s)


def string_size(address_string) -> tuple:
    """
    calculate the number of lines and the length of each line
    in that string
    :param address_string: the string representing thr address
    :return: a tuple with the first number the number of lines and
             the second a list of line lengths
    """
    num_lines = len(address_string.split("\n"))
    line_length = [len(line) for line in address_string.split("\n")]
    return num_lines, line_length


# create the sheet
sheet = Sheet(spec, write_address, border=False)

# let's just write the same address a bunch of times
label_count = spec.columns * spec.rows
address = "Test Name\nTest Address\nTest Address 2\nTest City, Test State, Test Zip"
for i in range(label_count):
    sheet.add_label(address)

sheet.save("test.pdf")
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))
