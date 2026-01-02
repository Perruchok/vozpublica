# Concept embeddings module
from postprocessing_helpers import embed_text


def get_concept_embedding(concept: str) -> list[float]:
    return embed_text(concept)
  