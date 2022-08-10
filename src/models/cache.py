from typing import Dict, Optional

from dataclasses import dataclass


@dataclass(slots=True, repr=True, kw_only=True)
class Cache:
    prefix: str


class MasterCache:
    def __init__(self):
        self.__cache: Dict[int, Cache] = {}

    def get_cache(self, __attr: int) -> Optional[Cache]:
        return self.__cache.get(__attr)
    
    def insert_cache(self, __attr: int, cache: Cache):
        self.__cache[__attr] = cache
