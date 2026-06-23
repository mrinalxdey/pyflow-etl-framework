import pytest
from pyflow.utils import load_config, get_engine
from sqlalchemy.engine import Engine


def test_load_config_yaml():
    config = load_config()
    assert isinstance(config, dict)

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("does_not_exist.yaml")

def test_load_config_invalid_extension(tmp_path):
    file = tmp_path / "config.txt"
    file.write_text("hello")

    with pytest.raises(ValueError):
        load_config(file)

def test_get_engine(sample_config, monkeypatch):
    monkeypatch.setenv("DB_USERNAME", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_password")

    engine = get_engine(sample_config)

    assert isinstance(engine, Engine)