class ChampionSr:
    def __init__(self, data: dict[str, list[str, int]]) -> None:
        self._data = data

    @property
    def rune_primary(self) -> list[int]:
        return self._data["rune_primary"]

    @property
    def rune_secondary(self) -> list[int]:
        return self._data["rune_secondary"]

    @property
    def spell(self) -> list[str]:
        return self._data["spell"]

    @property
    def skill_priority(self) -> list[str]:
        return self._data["skill_priority"]
