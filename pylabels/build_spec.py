from .constants import I2MM, SHEET_SIZES
from .specifications import Specification


def build_spec(label_name: str, spec_dictionary: dict[str, dict]) -> Specification:
    """Buld a specification from the dictionary we parsed in
    `build_label_def`.

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
    # here is a list of things that don't get multiplied by the mulitplier
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
