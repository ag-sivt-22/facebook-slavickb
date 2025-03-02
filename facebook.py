#! /usr/bin/env python

from __future__ import annotations
from collections import deque
from typing import Optional, Deque
import logging


myLogger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# @dataclass
class User:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.friends: list[User] = []


class Facebook:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def pridej_uzivatel(self, name: str) -> None:
        myLogger.debug(f"Adding {name} to the database")
        self._users[name] = User(name)

    def pridej_znamost(self, name1: str, name2: str) -> None:
        user1_node = self._users[name1]
        user2_node = self._users[name2]

        user1_node.friends.append(user2_node)
        user2_node.friends.append(user1_node)

    def jak_daleko(self, name1: str, name2: str) -> Optional[int]:
        myLogger.debug(f"\n\nTask: find the distance between {name1} and {name2}\n")
        if name1 not in self._users:
            raise KeyError(f"{name1} zatím uniká zuckerbergovým pařátům\nBuď osobu přidejte do systému, nebo hledejte jinou známost")
        elif name2 not in self._users:
            raise KeyError(f"{name1} zatím uniká zuckerbergovým pařátům\nBuď osobu přidejte do systému, nebo hledejte jinou známost")
        else:
            candidates: Deque[tuple[User, int]] = deque()
            loop_check: list[User] = []

            candidates.append((self._users[name1], 0))

            while candidates:
                suspect = candidates.popleft()
                myLogger.debug(f"\n\nCurrent suspect is {suspect[0].name} (distance of {suspect[1]})")
                if suspect[0].name == name2:
                    return suspect[1]
                else:
                    myLogger.debug(f"Because {suspect[0].name} ain't {name2}, we're gonna take a look at {suspect[0].name}'s friends\n")
                    for user in suspect[0].friends:
                        if user not in loop_check:
                            myLogger.debug(f"Lemme introduce {user.name} to our suspects")
                            if user.name == name2:
                                myLogger.debug(f"Oh hey, we found {name2}\n________________________________\n\n")
                                return suspect[1] + 1
                            else:
                                candidates.append((user, suspect[1] + 1))
                                loop_check.append(user)

        return None


# Vytvoření instance Facebooku
fb = Facebook()

# Seznam unikátních jmen
jmena = [
    "Adam", "Beata", "Cyril", "Dana", "Emil", "František", "Gabriela", "Hana", "Ivan", "Jana",
    "Karel", "Lenka", "Marek", "Nina", "Ondřej", "Petra", "Quentin", "Radka", "Stanislav", "Tereza",
    "Urbán", "Veronika", "Walter", "Xenie", "Yvona", "Zdeněk", "Alex", "Blanka", "Cecilie", "David"
]

# Vkládání známostí do Facebooku
for jmeno in jmena:
    fb.pridej_uzivatel(jmeno)

# Hardkodované známosti
znamosti = [
    ("Adam", "Beata"), ("Adam", "Cyril"), ("Beata", "Dana"),
    ("Cyril", "Emil"), ("Cyril", "František"), ("Dana", "Gabriela"),
    ("Emil", "Hana"), ("František", "Ivan"), ("Gabriela", "Jana"),
    ("Hana", "Karel"), ("Ivan", "Lenka"), ("Jana", "Marek"),
    ("Karel", "Nina"), ("Lenka", "Ondřej"), ("Marek", "Petra"),
    ("Nina", "Quentin"), ("Ondřej", "Radka"), ("Petra", "Stanislav"),
    ("Quentin", "Tereza"), ("Radka", "Urbán"), ("Stanislav", "Veronika"),
    ("Tereza", "Walter"), ("Urbán", "Xenie"), ("Veronika", "Yvona"),
    ("Walter", "Zdeněk"), ("Xenie", "Alex"), ("Yvona", "Blanka"),
    ("Zdeněk", "Cecilie"), ("Alex", "David"), ("Blanka", "Adam")
]

# Vkládání známostí do Facebooku
for clovek1, clovek2 in znamosti:
    fb.pridej_znamost(clovek1, clovek2)


# myLogger.debug(f"Seznam uživatelů: {fb._users.__str__()}")
# for clovek in fb._users:
#     myLogger.debug(fb._users.get(clovek))

jmeno1 = "Beata"
jmeno2 = "Walter"

myLogger.debug(f"{jmeno1} a {jmeno2} jsou od sebe daleko {fb.jak_daleko(jmeno1, jmeno2)}")
