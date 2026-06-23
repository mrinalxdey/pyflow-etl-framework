from pyflow.transformers import optimize_memory


def test_optimize_memory_preserves_rows(valid_df):
    original_rows = len(valid_df)

    df = optimize_memory(valid_df)

    assert len(df) == original_rows


def test_optimize_memory_returns_dataframe(valid_df):
    df = optimize_memory(valid_df)

    assert df is not None