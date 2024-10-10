from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


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
