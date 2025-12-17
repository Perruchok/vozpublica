import json
import numpy as np
import pandas as pd

from postprocessing_helpers import df_to_records_serializable


def test_df_to_records_serializable_basic():
    df = pd.DataFrame([
        {
            "doc_id": "2025-01-01-example",
            "created_at": pd.Timestamp("2025-01-01T12:34:56"),
            "count": np.int64(5),
            "score": np.float64(3.14),
            "meta": {"nested_ts": pd.Timestamp("2020-02-02T00:00:00")},
        }
    ])

    records = df_to_records_serializable(df)

    # should be a non-empty list of dicts
    assert isinstance(records, list) and len(records) == 1

    rec = records[0]
    # ensure Timestamp converted to ISO str
    assert isinstance(rec["created_at"], str)
    assert rec["created_at"].startswith("2025-01-01T12:34:56")

    # numpy types converted to native python types
    assert isinstance(rec["count"], int)
    assert isinstance(rec["score"], float)

    # nested timestamp in dict converted
    assert isinstance(rec["meta"]["nested_ts"], str)

    # JSON dumps should succeed
    json.dumps(records)


def test_df_to_records_serializable_with_none_and_lists():
    df = pd.DataFrame([
        {
            "doc_id": "2025-01-02",
            "created_at": None,
            "tags": ["a", "b", np.int64(2)],
        }
    ])

    records = df_to_records_serializable(df)
    assert isinstance(records[0]["created_at"], (type(None), str))
    assert isinstance(records[0]["tags"], list)
    # embedded numpy int should be converted
    assert isinstance(records[0]["tags"][2], int)


def test_df_to_records_serializable_nan_inf():
    df = pd.DataFrame([
        {
            "doc_id": "2025-01-03",
            "score": float('nan'),
            "other": float('inf')
        }
    ])

    records = df_to_records_serializable(df)
    # NaN/Inf should be converted to None to avoid non-compliant JSON
    assert records[0]["score"] is None
    assert records[0]["other"] is None


    def test_df_to_records_chunk_id_with_pd_NA():
        df = pd.DataFrame([
            {"doc_id": "2025-01-05", "chunk_id": pd.NA},
            {"doc_id": "2025-01-05", "chunk_id": 2.0},
        ])

        records = df_to_records_serializable(df)
        assert records[0]["chunk_id"] is None
        assert records[1]["chunk_id"] == 2 and isinstance(records[1]["chunk_id"], int)
import pandas as pd
import numpy as np
import postprocessing_helpers as ph


class DummyTable:
    def __init__(self, supabase, name):
        self.supabase = supabase
        self.name = name

    def upsert(self, records):
        # store records for assertion
        self.supabase.last_calls[self.name] = records
        return self
    def upsert(self, records, *args, **kwargs):
        # support optional on_conflict and other kwargs used by real client
        self.supabase.last_calls[self.name] = records
        return self

    def execute(self):
        return {"status": "ok"}


class DummySupabase:
    def __init__(self):
        self.last_calls = {}

    def table(self, name):
        return DummyTable(self, name)


def test_database_loading_serializes_timestamps_and_numpy(monkeypatch):
    dummy = DummySupabase()
    monkeypatch.setattr(ph, "supabase", dummy)

    raw = pd.DataFrame([
        {
            "doc_id": "2025-01-01-example",
            "created_at": pd.Timestamp("2025-01-01T12:34:56"),
            "meta": {"count": np.int64(5), "flag": np.bool_(True)}
        }
    ])

    embedded = pd.DataFrame([
        {
            "doc_id": "2025-01-01-example",
            "sequence": np.int64(1),
            "text": "Hola mundo",
            "embedding": np.array([1.0, 2.0, 3.0]),
            "created_at": pd.Timestamp("2025-01-01T12:34:56")
        }
    ])

    # Should not raise
    ph.database_loading(raw, embedded)

    # Validate raw table call
    assert "raw_transcripts" in dummy.last_calls
    raw_rec = dummy.last_calls["raw_transcripts"][0]
    # timestamps must be strings
    assert isinstance(raw_rec["created_at"], str)
    # numpy scalar inside dict must be converted to native python type
    assert isinstance(raw_rec["meta"]["count"], int)

    # Validate embedded table call
    assert "speech_turns" in dummy.last_calls
    emb_rec = dummy.last_calls["speech_turns"][0]
    assert isinstance(emb_rec["created_at"], str)
    # embedding numpy array must be converted to list
    assert isinstance(emb_rec["embedding"], list)
    assert all(isinstance(x, float) for x in emb_rec["embedding"]) 


def test_database_loading_dedupes(monkeypatch):
    dummy = DummySupabase()
    monkeypatch.setattr(ph, "supabase", dummy)

    raw = pd.DataFrame([])

    embedded = pd.DataFrame([
        {"doc_id": "A", "sequence": 1, "chunk_id": 1, "text": "one"},
        {"doc_id": "A", "sequence": 1, "chunk_id": 1, "text": "one-dup"},
        {"doc_id": "A", "sequence": 1, "chunk_id": None, "text": "nochunk"},
        {"doc_id": "A", "sequence": 1, "chunk_id": None, "text": "nochunk-dup"},
    ])

    # database_loading should NOT add a 'row_id' or 'speech_id' column on its own
    ph.database_loading(raw, embedded)
    assert "speech_turns" in dummy.last_calls
    records = dummy.last_calls["speech_turns"]
    assert all("row_id" not in r for r in records)


def test_add_speech_id_column_and_dedupe():
    df = pd.DataFrame([
        {"doc_id": "A", "sequence": 1, "chunk_id": 1},
        {"doc_id": "A", "sequence": 1, "chunk_id": 1.0},
        {"doc_id": "A", "sequence": 1, "chunk_id": pd.NA},
        {"doc_id": "B", "sequence": 2, "chunk_id": None},
    ])

    # add speech_id column
    df2 = ph.add_speech_id_column(df, column_name="speech_id")
    assert "speech_id" in df2.columns
    assert df2.loc[0, "speech_id"] == "A|1|1"
    assert df2.loc[1, "speech_id"] == "A|1|1"
    assert df2.loc[2, "speech_id"] == "A|1"
    assert df2.loc[3, "speech_id"] == "B|2"

    # now serializing and deduping
    records = df_to_records_serializable(df2)
    deduped = ph.dedupe_records_by_field(records, field="speech_id")
    ids = {r.get("speech_id") for r in deduped}
    # Expect unique ids for A|1|1 and A|1 and B|2 -> 3 total
    assert len(ids) == 3
