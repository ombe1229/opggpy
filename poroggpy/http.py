from typing import Any, Literal, Optional
from aiohttp import ClientSession
from types import TracebackType


class PoroggHttpClient:
    BASE_URL = "https://poro.gg"

    def __init__(self, session: Optional[ClientSession] = None) -> None:
        self.session = session

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def __aenter__(self) -> "PoroggHttpClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def request(
        self, method: Literal["GET"], endpoint: str, **kwargs: Any
    ) -> Any:
        if not self.session:
            self.session = ClientSession()

        async with self.session.request(
            method, self.BASE_URL + endpoint, **kwargs
        ) as r:
            return await r.text()

    async def get_champion_sr(
        self, champion: str, lane: Literal["top", "mid", "jng", "adc", "sup"]
    ) -> Any:
        return await self.request("GET", f"/champions/{champion}/sr/{lane}")
