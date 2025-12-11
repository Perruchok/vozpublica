import re
from typing import Tuple, Optional

# Keywords typically found in role/position texts (Spanish). Used for heuristics.
ROLE_KEYWORDS = [
    'PRESIDENT', 'PRESIDENTA', 'PRESIDENTE', 'SECRETAR', 'MINISTR', 'TITULAR', 'COORDINADOR', 'COORDINADORA',
    'JEFE', 'DIRECTOR', 'VOCER', 'VOCERA', 'SUBSECRETAR', 'PROCURAD', 'GOBERNADOR', 'ALCALDE', 'DIPUTADO',
    'SENADOR', 'REPRESENTANTE', 'RECTOR', 'DELEGADO', 'VOCES', 'VOZ', 'MODERADOR', 'MODERADORA', 'COORDINACIÓN',
    'SECRETARÍA', 'SECRETARIA', 'UNIDAD', 'DEPARTAMENTO', 'INSTITUTO', 'INSTITUTO', 'COMISION', 'COMISIÓN',
    'OFICIAL', 'PRESIDENCIA', 'CONSEJ', 'CONSEJERA', 'EMBAJADOR', 'EMBAJADORA', 'COMISARIO', 'TESORER', 'UIF', 'SHCP'
]

_ROLE_KEYWORDS_UPPER = set(k.upper() for k in ROLE_KEYWORDS)


def _count_role_keywords(text: str) -> int:
    text_u = text.upper()
    count = 0
    for kw in _ROLE_KEYWORDS_UPPER:
        if kw in text_u:
            count += 1
    return count


SP_NAME_STOPWORDS = {'DE', 'LA', 'DEL', 'Y', 'LOS', 'LAS', 'EL'}


def normalize_name(name: Optional[str]) -> Optional[str]:
    """Normalize a person name: title-case and trim extra whitespace.

    Preserves accents and punctuation. Returns None if name is falsy.
    """
    if not name:
        return None
    s = name.strip()
    # Remove trailing colons and stray punctuation
    s = re.sub(r'[:]+$', '', s).strip()
    # Lowercase then title-case keeps accents
    return ' '.join([w.capitalize() for w in s.title().split()])


def _title_case_keep_acronyms(text: str, original: str) -> str:
    """Return title-cased `text` but keep uppercase acronyms present in `original`.

    Example: original='... (UIF) ...' ensures UIF stays uppercase in the result.
    """
    t = text.title()
    # Find uppercase-acronyms in original (2-5 uppercase letters), but avoid
    # Spanish stopwords like DE/LA and long words like SECRETARIA.
    acronyms = {
        a for a in re.findall(r"\b([A-Z]{2,5})\b", original)
        if a not in SP_NAME_STOPWORDS
    }
    for acr in acronyms:
        t = re.sub(rf'(?i)\b{acr}\b', acr, t)
    return t


def parse_speaker_raw(sraw: Optional[str]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Parse a raw speaker string and try to return a 3-tuple:
      (speaker_raw, speaker_normalized, role_normalized)

    Heuristics used:
    - If there's a single comma, decide whether left/right are role/name using
      keyword matching and heuristics (name length, presence of parentheses/acronyms).
    - If multiple commas, try to treat the last portion as name (common pattern)
      unless role keywords appear strongly in the last chunk.
    - If no comma, make a best-effort guess: treat as name if short (<=3 words),
      otherwise as role.

    Returns speaker_raw exactly (trimmed & stripped of trailing colon), plus the
    normalized name and normalized role (title cased). If any part cannot be
    found, it returns None for that element.
    """
    if not sraw:
        return None, None, None

    original = sraw.strip()
    # strip trailing colon(s)
    s = re.sub(r'[:]+\s*$', '', original).strip()

    # Split on commas but keep parentheses tokens together
    parts = [p.strip() for p in s.split(',') if p.strip()]

    # Helper to count tokens that look like a personal name
    def name_score(p: str) -> int:
        tokens = [t for t in re.split(r"\s+", p) if t]
        # score tokens not in stopwords and that are reasonable short words (<=25 chars)
        score = 0
        for t in tokens:
            if t.upper() in SP_NAME_STOPWORDS:
                continue
            # treat tokens that are mostly alphabetic as name fragments
            if re.match(r"^[A-ZÁÉÍÓÚÑÀ-ÿ'\-]+$", t.upper()):
                score += 1
        return score

    # Decide pair(s)
    name_part = None
    role_part = None

    if len(parts) == 1:
        p = parts[0]
        tokens = p.split()

        # Special heuristic: strings like 'PRESIDENTA CLAUDIA SHEINBAUM PARDO'
        # (role followed immediately by name without comma) should be split
        # into role + name. We detect if the initial tokens contain role
        # keywords and the trailing tokens look like a personal name.
        if len(tokens) >= 3 and _count_role_keywords(tokens[0]) > 0:
            # Find the earliest split where the suffix looks like a name
            found = False
            for i in range(1, len(tokens)):
                tail = ' '.join(tokens[i:])
                # If the tail has at least two name-like tokens, treat as name
                if name_score(' '.join(tokens[i:i+2])) >= 2 or name_score(tail) >= 2:
                    role_part = ' '.join(tokens[:i])
                    name_part = tail
                    found = True
                    break
            if not found:
                # Fallback to previous heuristics below
                pass

        # If no split found above, use previous heuristics
        if name_part is None and role_part is None:
            # if it's short it's likely a name
            token_count = len(p.split())
            if token_count <= 3 and name_score(p) >= 2:
                name_part = p
            else:
                # perhaps it's a role or single-word name; we'll prefer name if looks like a personal name
                if name_score(p) >= 2:
                    name_part = p
                else:
                    role_part = p

    elif len(parts) == 2:
        left, right = parts

        # If right contains parenthesis or known acronyms it's very likely a role
        if re.search(r"\(|\b[A-Z]{2,}\b", right):
            # right looks like role if it contains acronyms or parentheses
            # but if right is short and looks very name-like, prefer name
            if name_score(right) >= 2 and len(right.split()) <= 3 and _count_role_keywords(right) == 0:
                # right is probably the name
                name_part = right
                role_part = left
            else:
                role_part = right
                name_part = left

        elif re.search(r"\(|\b[A-Z]{2,}\b", left):
            # left contains acronyms/parentheses -> left likely role
            role_part = left
            name_part = right

        else:
            # Neither side has parentheses: score using role keyword frequency and name-likeness
            left_role_score = _count_role_keywords(left)
            right_role_score = _count_role_keywords(right)

            left_name_score = name_score(left)
            right_name_score = name_score(right)

            # If either side has a stronger role score, pick it as role
            if left_role_score > right_role_score:
                role_part = left
                name_part = right
            elif right_role_score > left_role_score:
                role_part = right
                name_part = left
            else:
                # Tie: prefer the shorter side as name (names tend to be shorter), or last as name
                if len(right.split()) <= 3 and right_name_score >= max(1, left_name_score):
                    name_part = right
                    role_part = left
                elif len(left.split()) <= 3 and left_name_score >= max(1, right_name_score):
                    name_part = left
                    role_part = right
                else:
                    # fallback: last part is often name
                    name_part = right
                    role_part = left

    else:
        # More than 2 parts usually means the last chunk is the name (common), but check for role keywords
        last = parts[-1]
        preceding = ', '.join(parts[:-1])
        # If last looks like a name, accept
        if name_score(last) >= 2 and len(last.split()) <= 4:
            name_part = last
            role_part = preceding
        else:
            # try find any chunk that looks name-like
            for p in reversed(parts):
                if name_score(p) >= 2 and len(p.split()) <= 4:
                    name_part = p
                    others = parts.copy()
                    others.remove(p)
                    role_part = ', '.join(others)
                    break
            if name_part is None:
                # fallback: treat the last chunk as name
                name_part = last
                role_part = preceding

    # Post-process
    name_normalized = normalize_name(name_part) if name_part else None
    role_normalized = None
    if role_part:
        # title-case but preserve existing acronyms from original
        role_normalized = _title_case_keep_acronyms(role_part, role_part)
        role_normalized = role_normalized.strip()

    # Return sraw(original), normalized name and normalized role
    return original, name_normalized, role_normalized


if __name__ == "__main__":
    examples = [
        "SECRETARIA DE TURISMO, JOSEFINA RODRÍGUEZ ZAMORA",
        "PABLO GÓMEZ ÁLVAREZ, TITULAR DE LA UNIDAD DE INTELIGENCIA FINANCIERA (UIF) DE LA SECRETARÍA DE HACIENDA Y CRÉDITO PÚBLICO (SHCP):",
        "COORDINADORA DE LOS TRABAJOS DEL GOBIERNO FEDERAL PARA EL MUNDIAL 2026, GABRIELA CUEVAS BARRON",
        "MODERADOR:"
    ]
    for ex in examples:
        print(parse_speaker_raw(ex))
