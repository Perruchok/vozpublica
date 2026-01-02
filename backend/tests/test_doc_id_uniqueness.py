import pandas as pd
from scraper_helpers import add_articles_metadata


def test_duplicate_doc_id_suffixing():
    # Two articles that would generate the same base doc_id
    articles = [
        {"href": "https://example.com/a1", "published_at": "2025-11-15T10:00:00-06:00", "title": "Evento: conferencia de prensa de la presidenta Claudia Sheinbaum Pardo"},
        {"href": "https://example.com/a2", "published_at": "2025-11-15T11:00:00-06:00", "title": "Evento: conferencia de prensa de la presidenta Claudia Sheinbaum Pardo"},
        {"href": "https://example.com/a3", "published_at": "2025-11-15T12:00:00-06:00", "title": "Otra noticia cualquiera"},
        {"href": "https://example.com/a4", "published_at": "2025-11-15T13:00:00-06:00", "title": "Otra noticia cualquiera"},
    ]

    df = add_articles_metadata(articles)

    # Build expected prefixes
    expected_first = "2025-11-15-mananera"
    expected_second = "2025-11-15-mananera2"

    # For the other pair, 'conference' suffix applies.
    expected_third = "2025-11-15-conference"
    expected_fourth = "2025-11-15-conference2"

    ids = df['doc_id'].tolist()

    assert ids[0] == expected_first
    assert ids[1] == expected_second
    assert ids[2] == expected_third
    assert ids[3] == expected_fourth
