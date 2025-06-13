import json
from pathlib import Path
from typing import Any


def load_json_data(path: Path) -> dict[str, Any]:
    """Load and parse a JSON file into a dictionary."""
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_image_path(source_filename: Path) -> str:
    """Helper for constructing the relative image path from BVQA json filenames.

    Filesystem layout for the application should be of the form:

    images/
    ├── APV0001/
    │   └── APV0001_page1_image1.jpg
    └── APV0002/
        └── APV0002_page1_image1.jpg

    Example:
        Expected JSON filename: APV01_page8_img1_b102r.jpg_644894.qas.json
        Corresponding image file path: APV01/APV01_page8_img1_b102r.jpg

    Then in the .env file you point the application to the 'images' folder:
    IMAGES_DIR=/my/path/to/images

    Deprecated from version BVQA 1e0666c onwards when the relative path to images
    will be available in the body of the json.
    See: https://github.com/kingsdigitallab/kdl-vqa/issues/30
    """
    json_filename = Path(source_filename)

    stem = json_filename.stem
    parts = stem.split(".")

    image_name = parts[0] + "." + parts[1].split("_")[0]
    image_dir = parts[0].split("_")[0]

    return str(Path(image_dir) / image_name)
