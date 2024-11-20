pylabels2
=========

``pylabels2`` is a Python library for creating PDFs to print sheets of labels. It
uses the [ReportLab PDF toolkit][1] to produce the PDF.

This is a fork of [davis-junior/pylabels](https://github.com/davis-junior/pylabels)

The original project was written by Blair Bonnett found at [bcbnz/pylabels](https://github.com/bcbnz/pylabels)

Installation
============

    pip install pylabels2

Usage
=====

Note: In this fork, the module has been renamed from ``labels`` to ``pylabels``.

Install:

    from pylabels import Specification, Sheet

Create a ``callable`` that adds content to a single label:

    def draw_label(label, width, height, label_data):
        label.add(shapes.String(2, 2, str(label_data), fontName="Helvetica", fontSize=40))

Create a ``Specification`` for the layout of the labels on a sheet:

    specs = Specification(210, 297, 2, 8, 90, 25, corner_radius=2)

Create a ``Sheet`` and pass it the ``spec`` and ``callable``:

    sheet = Sheet(specs, draw_label, border=True)

Add labels to the ``sheet``:

    sheet.add_label("Hello World1")
    sheet.add_label("Hello World2")
    # etc ...

Save the ``sheet`` to file as PDF:

    sheet.save("basic.pdf")

Or save to BytesIO buffer:

    buffer = sheet.save_to_buffer()

See detailed examples below.

Overview
========
Basically, the user creates a set of specifications of the label sizes etc,
writes a callback function which does the actual drawing, and gives these two
items to a Sheet object. Items are then added to the sheet using the
add_label() method (or add_labels() to add all items from an iterable).

The callback function is called once for each item, being given a ReportLab
Drawing object representing the label, its width and height, and the item to
draw on the label. Any of the standard ReportLab drawing methods can be used,
with pylabels automatically adding a clipping path around each label to prevent
it interfering with other labels.

Once all the items have been added, the labels can be saved as a PDF, a
preview of a page can be saved as an image, or returned as a BytesIO buffer.

[1]: http://www.reportlab.com/opensource/

Examples
========

The following examples are available in the demos directory:

* [Basic](pylabels/demos/basic.py) - a introduction to the basic use of pylabels.
* [Partial pages](pylabels/demos/partial_page.py) - how to produce partial pages (i.e.,
  pages with some of the labels previously used).
* [Repeated](pylabels/demos/repeated.py) - how to use the count parameter to add
  multiple copies of the same label.
* [Background colours](pylabels/demos/background_colours.py) - examples of solid,
  striped and hatched backgrounds of different colours on each label.
* [Page background](pylabels/demos/page_background.py) - how to add a background
  image for each page.
* [Padding](pylabels/demos/padding.py) - how to add padding to the labels.
* [Nametags](pylabels/demos/nametags.py) - creates a set of nametags from the list of
  names in the names.txt file. Includes the use of two custom fonts, font size
  selection, and centred text.
* [Image preview](pylabels/demos/preview.py) - generates image previews of two of the
  pages from the nametags demo.
* [Addresses](pylabels/demos/addresses.py) - print mailing labels (From a CSV file) on a
  standard Avery 5160 label page.
* [Django demo](pylabels/demos/django_demo/project) - Download a PDF of labels with barcodes
  directly from the browser in a [Django](https://www.djangoproject.com) project
  (uses ``save_to_buffer`` instead of ``save``).


Demo fonts
==========

The following fonts are used in the demo scripts and are included in the demos
folder:

* Judson Bold - http://openfontlibrary.org/en/font/judson (Open Font License)
* KatamotzIkasi - http://openfontlibrary.org/en/font/katamotzikasi (GPL)

License
=======

Copyright (C) 2012, 2013, 2014, 2015 Blair Bonnett

pylabels is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

pylabels is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
pylabels.  If not, see <http://www.gnu.org/licenses/>.
