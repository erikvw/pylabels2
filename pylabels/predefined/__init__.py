from __future__ import annotations

import os
from importlib import import_module
from inspect import isclass
from warnings import warn

from ..specifications import Specification

LETTER_PORTRAIT_WIDTH = 215.9
LETTER_PORTRAIT_HEIGHT = 279.4
LETTER_LANDSCAPE_WIDTH = LETTER_PORTRAIT_HEIGHT
LETTER_LANDSCAPE_HEIGHT = LETTER_PORTRAIT_WIDTH


class _PredefinedSpec(Specification):
    """Classes derived from this one can specify dimensions as class
    variables.

    All dimensions should be specified from a "portrait" perspective.
    The landscape class method will automatically transpose these
    dimensions if a landscape orientation is needed.
    """

    _CALLED_FROM_CLASSMETHOD = False

    def __init__(self, *args, **kwargs):
        # Encourage the caller to use a factory method instead
        # of calling __init__ directly.
        if not self._CALLED_FROM_CLASSMETHOD:
            warn(
                "This specification should only be created using a "
                "class method ('portrait' or 'landscape')"
            )

        super().__init__(*args, **kwargs)

        # Reset our internal call marker.
        _PredefinedSpec._CALLED_FROM_CLASSMETHOD = False

    @classmethod
    def portrait(cls):
        cls._CALLED_FROM_CLASSMETHOD = True
        return cls(
            sheet_width=LETTER_PORTRAIT_WIDTH,
            sheet_height=LETTER_PORTRAIT_HEIGHT,
            columns=getattr(cls, "COLUMNS", None),
            rows=getattr(cls, "ROWS", None),
            label_width=getattr(cls, "LABEL_WIDTH", None),
            label_height=getattr(cls, "LABEL_HEIGHT", None),
            corner_radius=getattr(cls, "CORNER_RADIUS", None),
            top_margin=getattr(cls, "TOP_MARGIN", None),
            bottom_margin=getattr(cls, "BOTTOM_MARGIN", None),
            left_margin=getattr(cls, "LEFT_MARGIN", None),
            right_margin=getattr(cls, "RIGHT_MARGIN", None),
            row_gap=getattr(cls, "ROW_GAP", None),
            column_gap=getattr(cls, "COLUMN_GAP", None),
        )

    @classmethod
    def landscape(cls):
        cls._CALLED_FROM_CLASSMETHOD = True
        return cls(
            sheet_width=LETTER_LANDSCAPE_WIDTH,
            sheet_height=LETTER_LANDSCAPE_HEIGHT,
            columns=getattr(cls, "ROWS", None),
            rows=getattr(cls, "COLUMNS", None),
            label_width=getattr(cls, "LABEL_HEIGHT", None),
            label_height=getattr(cls, "LABEL_WIDTH", None),
            corner_radius=getattr(cls, "CORNER_RADIUS", None),
            top_margin=getattr(cls, "LEFT_MARGIN", None),
            bottom_margin=getattr(cls, "RIGHT_MARGIN", None),
            left_margin=getattr(cls, "TOP_MARGIN", None),
            right_margin=getattr(cls, "BOTTOM_MARGIN", None),
            row_gap=getattr(cls, "COLUMN_GAP", None),
            column_gap=getattr(cls, "ROW_GAP", None),
        )


def all_predefined_specs():
    """Return an iterator for all predefined specs. The objects
    returned by the iterator are tuples containing the spec name
    as a string and the spec class as an object.
    """

    # Inspect all files in this file's directory
    for py_file in sorted(os.listdir(os.path.dirname(__file__))):

        # If it's a py file and not a under/dunder file,
        # it may contain specifications
        if py_file.endswith(".py") and not py_file.startswith("_"):

            # Import the file so we can inspect it.
            py_module, _ = os.path.splitext(py_file)
            imported = import_module("labels.predefined." + py_module)

            for member_name, member_value in sorted(vars(imported).items()):
                # If we find a public class derived from _PredefinedSpec, yield.
                if (
                    not member_name.startswith("_")
                    and isclass(member_value)
                    and issubclass(member_value, _PredefinedSpec)
                ):
                    yield ".".join([py_module, member_name]), member_value
