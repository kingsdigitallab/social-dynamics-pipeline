import json
from pathlib import Path

import pytest

from pipeline.tasks.utils.db_import_utils import get_image_path, load_json_data


@pytest.mark.parametrize(
    "source_filename, expected_image_name",
    [
        # Standard expected case
        (
            Path("APV01_page8_img1_b102r.jpg_644894.qas.json"),
            "APV01/APV01_page8_img1_b102r.jpg",
        ),
    ],
)
def test_get_image_path(source_filename, expected_image_name):
    assert get_image_path(source_filename) == expected_image_name


def test_load_json_data(tmp_path: Path):
    test_data = {"key": "value", "nested": {"a": 1, "b": 2}}
    test_file = tmp_path / "sample.json"
    test_file.write_text(json.dumps(test_data), encoding="utf-8")
    result = load_json_data(test_file)
    assert isinstance(result, dict)
    assert result == test_data


def test_load_json_data_missing_file(tmp_path: Path):
    missing_file = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_json_data(missing_file)
