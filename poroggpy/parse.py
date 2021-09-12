from bs4 import BeautifulSoup
import regex
import static_data

from poroggpy.http import PoroggHttpClient
from poroggpy.static import SoupAttr


class PoroggParser:
    def __init__(self):
        self.http_client = PoroggHttpClient()
        self.ddragon = static_data.ddragon()
        self.soup_attr = SoupAttr()

    def slice_url(self, url: str) -> str:
        re = regex.compile(r"(?<=/|[/0-9_])[a-zA-Z]+(?=\.png)")
        return re.search(url).group()

    async def parse_ch_sr(self, content):
        data = {}
        soup = BeautifulSoup(content, "html.parser")

        rune_div = soup.find(
            "div",
            self.soup_attr.rune,
        )
        primary = rune_div.find("div", self.soup_attr.rune_primary)
        primary_active = primary.find_all("img", {"class": "active"})
        data["rune_primary"] = [
            self.ddragon.getRune(self.slice_url(i["src"])).id for i in primary_active
        ]  # [8100, 8200, 8300, 8400, 8500]
        secondary = rune_div.find("div", self.soup_attr.rune_secondary)
        secondary_active = secondary.find_all("img", {"class": "active"})
        data["rune_secondary"] = [
            self.ddragon.getRune(self.slice_url(i["src"])).id for i in secondary_active
        ]  # [8100, 8200, 8300]

        spell_div = soup.find("div", self.soup_attr.spell)
        spell_img = spell_div.find_all("img")
        data["spell"] = [
            self.slice_url(i["src"]) for i in spell_img
        ]  # [SummonerSmite, SummonerFlash]

        skill_div = soup.find("div", self.soup_attr.skill)
        skills = skill_div.find_all("div", {"class": "champion__skill"})
        data["skill"] = [skill.find("span").text for skill in skills]  # [Q, E, W]


class ChampionSr:
    def __init__(self, data):
        self.data = {
            "spell": data["spell"],
            "item": data["item"],
            "skill": data["skill"],
            "rune_primary": data["rune_primary"],
            "rune_sub": data["rune_sub"],
        }

    @property
    def spell(self) -> list[str]:
        return self.data["spell"]

    @property
    def item(self) -> list[str]:
        return self.data["item"]

    @property
    def skill(self) -> list[str]:
        return self.data["skill"]

    @property
    def rune_primary(self) -> list[str]:
        return self.data["rune_primary"]

    @property
    def rune_sub(self) -> list[str]:
        return self.data["rune_sub"]
