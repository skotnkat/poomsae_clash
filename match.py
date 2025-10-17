from typing import Optional

from athlete import Athlete
from poomsae import Poomsae
from draw_poomsae import (
    draw_poomsae,
    get_poomsae_intersection,
)


class Match:
    def __init__(
        self,
        match_id: int,
        first_athlete: Athlete,
        second_athlete: Athlete,
        first_poomsae: Optional[Poomsae],
        second_poomsae: Optional[Poomsae],
    ) -> None:
        self.match_id = int(match_id)
        self.first_athlete = first_athlete
        self.second_athlete = second_athlete
        self.winner_id = None
        self.first_poomsae = first_poomsae
        self.second_poomsae = second_poomsae

    def draw_poomsae_for_match(self) -> None:
        if self.first_poomsae is not None and self.second_poomsae is not None:
            return

        min_poomsae, max_poomsae = get_poomsae_intersection(
            self.first_athlete, self.second_athlete
        )
        first_poomsae = draw_poomsae(
            min_poomsae,
            max_poomsae,
        )

        second_poomsae = draw_poomsae(
            min_poomsae, max_poomsae, prev_poomsae=first_poomsae
        )

        self.first_poomsae = first_poomsae
        self.second_poomsae = second_poomsae
