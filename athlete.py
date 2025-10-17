import datetime
from poomsae import Poomsae

CUR_YEAR = datetime.datetime.now().year

JUNIOR_RANGE = range(CUR_YEAR - 17, CUR_YEAR - 14)  # 15-17 years old


def get_min_poomsae(birth_year: int, belt_category: str) -> int:
    if belt_category == "B":
        return 4

    if birth_year in JUNIOR_RANGE:
        return 5

    return 7  # Seniors


class Athlete:
    def __init__(
        self,
        athlete_id: int,
        first_name: str,
        last_name: str,
        birth_year: int,
        category: str,
        max_poomsae: Poomsae,
    ) -> None:
        self.athlete_id = int(athlete_id)
        self.first_name = first_name
        self.last_name = last_name

        self.min_poomsae = Poomsae(number=get_min_poomsae(birth_year, category))
        self.max_poomsae = max_poomsae

    def __repr__(self) -> str:
        return f"Athlete(id={self.athlete_id}, name={self.first_name} {self.last_name}, min_poomsae={self.min_poomsae}, max_poomsae={self.max_poomsae})"
