from typing import Optional

POOMSAE_NUMBER_TO_NAME_MAP = {
    4: "Taeguk 4",
    5: "Taeguk 5",
    6: "Taeguk 6",
    7: "Taeguk 7",
    8: "Taeguk 8",
    9: "Koryo",
    10: "Keumgang",
    11: "Taebek",
    12: "Pyongwon",
    13: "Sipjin",
    14: "Jitae",
    15: "Chongwon",
    16: "Hansoo",
    17: "Ilyo",
}

POOMSAE_NAME_TO_NUMBER_MAP = {v: k for k, v in POOMSAE_NUMBER_TO_NAME_MAP.items()}


class Poomsae:
    def __init__(
        self, name: Optional[str] = None, number: Optional[int] = None
    ) -> None:
        if name is None and number is None:
            raise ValueError("Either name or number must be provided")

        if number is not None:
            if number not in POOMSAE_NUMBER_TO_NAME_MAP:
                raise ValueError(f"Invalid poomsae number: {number}")
            self.poomsae_id = number
            self.poomsae_name = POOMSAE_NUMBER_TO_NAME_MAP[number]
            # Validate name matches if both provided
            if name is not None and self.poomsae_name != name:
                raise ValueError("Provided name and number do not match")
        else:
            # Only name is provided
            if name not in POOMSAE_NAME_TO_NUMBER_MAP:
                raise ValueError(f"Invalid poomsae name: {name}")
            self.poomsae_name = name
            self.poomsae_id = POOMSAE_NAME_TO_NUMBER_MAP[name]

    def number(self) -> int:
        return int(self.poomsae_id)

    def name(self) -> str:
        return str(self.poomsae_name)

    def __repr__(self) -> str:
        return self.name()

    def __lt__(self, other) -> bool:
        if isinstance(other, Poomsae):
            return self.number() < other.number()
        return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, Poomsae):
            return self.number() <= other.number()
        return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, Poomsae):
            return self.number() > other.number()
        return NotImplemented

    def __ge__(self, other) -> bool:
        if isinstance(other, Poomsae):
            return self.number() >= other.number()
        return NotImplemented

    def __eq__(self, other) -> bool:
        if isinstance(other, Poomsae):
            return self.number() == other.number()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.number())
