from typing import Literal, Optional

from aiohttp.client import ClientSession
from poroggpy.http import PoroggHttpClient
from poroggpy.parser import PoroggParser
from poroggpy.models.champion_sr import ChampionSr


class Porogg(PoroggHttpClient):
    def __init__(self, session: Optional[ClientSession] = None) -> None:
        super().__init__(session)
        self.parser = PoroggParser()

    async def ch_sr(
        self, champion: str, lane: Literal["top", "jng", "mid", "adc", "sup"]
    ) -> ChampionSr:
        html = await self.get_ch_sr(champion, lane)
        return ChampionSr(self.parser.parse_ch_sr(html))
