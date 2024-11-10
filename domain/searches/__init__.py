from typing import Dict, Type

from configs.domain import configs
from domain.searches.base import BaseSearch
from domain.searches.qwen import QWen215BInstructSearch
from domain.searches.stella import StellaEn15BV5Search

mapping: Dict[str, Type[BaseSearch]] = {
    "qwen": QWen215BInstructSearch,
    "stella": StellaEn15BV5Search,
}

model = mapping[configs.search_model]
