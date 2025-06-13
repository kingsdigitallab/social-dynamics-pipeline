import json
from pathlib import Path
from typing import Any


def load_json_data(path: Path) -> dict[str, Any]:
    """Load and parse a JSON file into a dictionary."""
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_image_name(source_filename: Path):
    """Helper for stripping the image filename from BVQA json filenames.

    Deprecated from version BVQA 1e0666c onwards when the relative path to images
    will be available in the body of the json.
    See: https://github.com/kingsdigitallab/kdl-vqa/issues/30
    """
    img_path = Path(source_filename)
    img_frags = img_path.stem.split(".")
    img_stem = img_frags[0]
    img_ext = img_frags[1].split("_")[0]
    image_name = img_stem + "." + img_ext
    return image_name
