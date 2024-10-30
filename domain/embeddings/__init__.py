from typing import Dict, Type

from configs.domain import configs
from domain.embeddings.base import BaseEmbedding
from domain.embeddings.qwen import QWen215BInstructEmbedding
from domain.embeddings.stella import StellaEn15BV5Embedding

mapping: Dict[str, Type[BaseEmbedding]] = {
    "qwen": QWen215BInstructEmbedding,
    "stella": StellaEn15BV5Embedding,
}

model = mapping[configs.embedding_model]
