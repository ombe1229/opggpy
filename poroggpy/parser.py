from typing import Union
from bs4 import BeautifulSoup
import re
import static_data


class PoroggParser:
    def __init__(self):
        self.ddragon = static_data.ddragon()

    @staticmethod
    def slice_url(url: str) -> str:
        reg = re.compile(r"(?<=/|[/0-9_])[a-zA-Z]+(?=\.png)")
        return reg.search(url).group()

    async def parse_ch_sr(self, content: str) -> dict[str, list[Union[str, int]]]:
        data = {}
        soup = BeautifulSoup(content, "html.parser")

        rune_div = soup.find(
            "div",
            rune={
                "class": "champion-rune-tab-content active h-auto has-more",
                "data-tab-name": "default",
            },
        )

        primary = rune_div.find(
            "div", {"class": "champion-rune-build champion-rune-build--primary"}
        )
        primary_active = primary.find_all("img", {"class": "active"})
        data["rune_primary"] = [
            self.ddragon.getRune(self.slice_url(i["src"])).id for i in primary_active
        ]  # [8100, 8200, 8300, 8400, 8500]

        secondary = rune_div.find(
            "div", {"class": "champion-rune-build champion-rune-build--secondary"}
        )
        secondary_active = secondary.find_all("img", {"class": "active"})
        data["rune_secondary"] = [
            self.ddragon.getRune(self.slice_url(i["src"])).id for i in secondary_active
        ]  # [8100, 8200, 8300]

        spell_div = soup.find(
            "div",
            {
                "class": "champion-build champion-build--spells",
            },
        )
        spell_img = spell_div.find_all("img")
        data["spell"] = [
            self.slice_url(i["src"]) for i in spell_img
        ]  # [SummonerSmite, SummonerFlash]

        skill_div = soup.find(
            "div",
            skill={
                "class": "champion-skills__priority",
            },
        )
        skills = skill_div.find_all("div", {"class": "champion__skill"})
        data["skill_priority"] = [
            skill.find("span").text for skill in skills
        ]  # [Q, E, W]

        return data
