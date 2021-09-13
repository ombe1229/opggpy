from poroggpy.http import PoroggHttpClient
from poroggpy.parser import PoroggParser
from poroggpy.models.champion_sr import ChampionSr


class Porogg:
    def __init__(self) -> None:
        self.http = PoroggHttpClient()
        self.parser = PoroggParser()

    async def get_ch_build(self, champion, lane):
        html = await self.http.get_ch_sr(champion, lane)
        return ChampionSr(await self.parser.parse_ch_sr(html))
