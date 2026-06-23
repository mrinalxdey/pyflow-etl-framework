import pytest
from pyflow.validators import validate_csv_structure
from pyflow.utils import ValidationError


from pyflow.validators import validate_csv_structure


def test_validate_valid_csv(tmp_path, error_file):
    file = tmp_path / "valid.csv"

    file.write_text(
        "id,name\n"
        "1,Alice\n"
        "2,Bob\n"
    )

    bad_rows = validate_csv_structure(
        file,
        encoding="utf-8",
        error_file=error_file
    )

    assert bad_rows == 0

def test_validate_one_bad_row(tmp_path, error_file):
    file = tmp_path / "bad.csv"

    file.write_text(
        "id,name\n"
        "1,Alice\n"
        "2\n"
    )

    bad_rows = validate_csv_structure(
        file,
        encoding="utf-8",
        error_file=error_file
    )

    assert bad_rows == 1

def test_validate_multiple_bad_rows(tmp_path, error_file):
    file = tmp_path / "bad.csv"

    file.write_text(
        "id,name\n"
        "1\n"
        "2,Bob,Extra\n"
        "3,Charlie\n"
    )

    bad_rows = validate_csv_structure(
        file,
        encoding="utf-8",
        error_file=error_file
    )

    assert bad_rows == 2

def test_error_file_created(tmp_path, error_file):
    file = tmp_path / "bad.csv"

    file.write_text(
        "id,name\n"
        "1\n"
    )

    validate_csv_structure(
        file,
        encoding="utf-8",
        error_file=error_file
    )

    assert error_file.exists()