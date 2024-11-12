from typing import Dict, Type

from configs.domain import configs
from domain.model_types import SearchModelType
from domain.searches.base import BaseSearch
from domain.searches.qwen import QWen215BInstructSearch
from domain.searches.stella import StellaEn15BV5Search

mapping: Dict[SearchModelType, Type[BaseSearch]] = {
    SearchModelType.QWEN: QWen215BInstructSearch,
    SearchModelType.STELLA: StellaEn15BV5Search,
}

model = mapping[configs.search_model]
