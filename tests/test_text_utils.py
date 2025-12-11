from text_utils import parse_speaker_raw


def test_secretaria_name_role():
    sraw = "SECRETARIA DE TURISMO, JOSEFINA RODRÍGUEZ ZAMORA"
    raw, name, role = parse_speaker_raw(sraw)
    assert raw == sraw
    assert name == "Josefina Rodríguez Zamora"
    assert role == "Secretaria De Turismo"


def test_pablo_titular_complex():
    sraw = "PABLO GÓMEZ ÁLVAREZ, TITULAR DE LA UNIDAD DE INTELIGENCIA FINANCIERA (UIF) DE LA SECRETARÍA DE HACIENDA Y CRÉDITO PÚBLICO (SHCP):"
    raw, name, role = parse_speaker_raw(sraw)
    assert raw.startswith("PABLO GÓMEZ ÁLVAREZ")
    assert name == "Pablo Gómez Álvarez"
    # role should contain UIF and SHCP acronyms preserved
    assert "UiF" not in role and "UIF" in role
    assert "SHCP" in role


def test_coord_gabriela():
    sraw = "COORDINADORA DE LOS TRABAJOS DEL GOBIERNO FEDERAL PARA EL MUNDIAL 2026, GABRIELA CUEVAS BARRON"
    raw, name, role = parse_speaker_raw(sraw)
    assert name == "Gabriela Cuevas Barron"
    assert role.startswith("Coordinadora De Los Trabajos")


def test_presidenta_without_comma():
    sraw = "PRESIDENTA CLAUDIA SHEINBAUM PARDO"
    raw, name, role = parse_speaker_raw(sraw)
    assert name == "Claudia Sheinbaum Pardo"
    assert role == "Presidenta"


def test_presidenta_de_mexico_with_comma():
    sraw = "PRESIDENTA DE MÉXICO, CLAUDIA SHEINBAUM PARDO"
    raw, name, role = parse_speaker_raw(sraw)
    assert name == "Claudia Sheinbaum Pardo"
    assert role == "Presidenta De México"
from text_utils import parse_speaker_raw


def test_parse_speaker_normalization_example():
    raw = "SECRETARIA DE TURISMO, JOSEFINA RODRÍGUEZ ZAMORA"
    speaker_raw, speaker_normalized, role = parse_speaker_raw(raw)

    assert speaker_raw == raw
    assert speaker_normalized == "Josefina Rodríguez Zamora"
    assert role == "Secretaria De Turismo"
