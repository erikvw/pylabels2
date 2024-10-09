from pylabels.predefined import _PredefinedSpec


class A22822(_PredefinedSpec):
    """Specification for Avery 22822, 2" x 3" labels, 10 per sheet, 8.5"x11" paper size."""

    COLUMNS = 2
    ROWS = 4
    LABEL_WIDTH = 78
    LABEL_HEIGHT = 50.8
    CORNER_RADIUS = 4
    ROW_GAP = 3
    LEFT_MARGIN = 21.5
    COLUMN_GAP = 20.25
