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

import csv
from collections import namedtuple

from reportlab.graphics import shapes

from pylabels import Sheet, Specification

# Createa a labels page, matching Avery 5160, 8160, 6240, etc.

PADDING = 1
specs = Specification(
    215.9,
    279.4,
    3,
    10,
    64,
    25.4,
    corner_radius=2,
    left_margin=5,
    right_margin=5,
    top_margin=13,
    left_padding=PADDING,
    right_padding=PADDING,
    top_padding=PADDING,
    bottom_padding=PADDING,
    row_gap=0,
)

Address = namedtuple(
    "Address", ["name", "name2", "street1", "street2", "city", "state", "zip"]
)


def draw_address(label, width, height, address) -> None:
    assert address.state, address  # nosec B101
    assert address.zip, address  # nosec B101

    # The order is flipped, because we're painting from bottom to top.
    # The sum of the lines get .upper(), because that's what the USPS likes.
    lines = [
        ("%s %s  %s" % (address.city, address.state, address.zip)).upper(),
        address.street2.upper(),
        address.street1.upper(),
        address.name2,
        address.name,
    ]

    group = shapes.Group()
    x, y = 0, 0
    for line in lines:
        if not line:
            continue
        shape = shapes.String(x, y, line, textAnchor="start")
        _, _, _, y = shape.getBounds()
        # Some extra spacing between the lines, to make it easier to read
        y += 3
        group.add(shape)
    _, _, lx, ly = label.getBounds()
    _, _, gx, gy = group.getBounds()

    # Make sure the label fits in a sticker
    assert gx <= lx, (address, gx, lx)  # nosec B101
    assert gy <= ly, (address, gy, ly)  # nosec B101

    # Move the content to the center of the sticker
    dx = (lx - gx) / 2
    dy = (ly - gy) / 2
    group.translate(dx, dy)

    label.add(group)


sheet = Sheet(specs, draw_address, border=False)

filename = "addresses.csv"
with open(filename, newline="") as csvfile:
    reader = csv.DictReader(csvfile, Address._fields, quotechar='"')
    for row in reader:
        # Make sure we got all fields, and no extra fields.
        assert None not in row, row["name"]  # nosec B101
        assert "zip" in row, row["name"]  # nosec B101
        for k, v in row.items():
            row[k] = v.strip()

        address = Address(**row)

        sheet.add_label(address)


sheet.save("labels.pdf")
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))
