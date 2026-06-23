from pyflow.extractors import CSVExtractor


def test_extract_csv(sample_csv, sample_config):
    extractor = CSVExtractor(sample_config)

    chunk = next(extractor.extract(str(sample_csv)))

    assert not chunk.empty


def test_extract_csv_row_count(sample_csv, sample_config):
    extractor = CSVExtractor(sample_config)

    chunk = next(extractor.extract(str(sample_csv)))

    assert len(chunk) == 3


def test_extract_csv_columns(sample_csv, sample_config):
    extractor = CSVExtractor(sample_config)

    chunk = next(extractor.extract(str(sample_csv)))

    assert list(chunk.columns) == ["id", "name"]