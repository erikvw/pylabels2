from __future__ import annotations

import json
from pathlib import Path


def build_label_def(json_file_path: Path | str) -> dict[str, dict] | None:
    """Converts a JSON file of specifications per label into a
    dictionary of specifications per label.

    Each dictionary contains parameters to build a Specification
    instance.

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
