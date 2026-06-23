import os


def test_table_name_generation():
    file_name = "yellow_tripdata_2024-01.csv"

    table_name = (
        os.path.splitext(file_name)[0]
        .replace("-", "_")
        .replace(" ", "_")
    )

    assert table_name == "yellow_tripdata_2024_01"


def test_table_name_spaces():
    file_name = "my file.csv"

    table_name = (
        os.path.splitext(file_name)[0]
        .replace("-", "_")
        .replace(" ", "_")
    )

    assert table_name == "my_file"