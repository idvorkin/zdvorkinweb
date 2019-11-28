from collections import namedtuple
from typing import List, Set, Any
from dataclasses import dataclass, field
import re


@dataclass
class Passage:
    title: str = ""
    found_passage: bool = field(default_factory=bool)
    outgoing: List[Any] = field(default_factory=list)
    incoming: List[Any] = field(default_factory=list)

    def __repr__(self):
        return f"ID:{id(self)} Passage:{self.title}, cO:{len(self.outgoing)},cI:{len(self.incoming)}"


"""
    def __hash__(self):
        # print(f"hash:{self.title}")
        return (
            hash(self.title) + hash(tuple(self.incoming)) + hash(tuple(self.outgoing))
        )



    def __eq__(self, other):
        return self.title == other.title

"""


# def __repr__(self):
# return f"T:{self.title}\nout:{self.outgoing}\nin:{self.incoming}\n"


def orphanPassages(passages: List[Passage]) -> List[Passage]:
    return [p for p in passages if len(p.incoming) == 0]


def deadLinks(passages: List[Passage]) -> List[Passage]:
    return [p for p in passages if p.found_passage == False]


def validate(lines: List[str]):
    passages = extractPassages(lines)

    for passage in orphanPassages(passages):
        print(f"orphan:{passage.title}")

    for passage in deadLinks(passages):
        print(f"dead_link:{passage.title}")

    return


def extractPassages(lines: List[str]) -> List[Passage]:
    def parsePassage(line):
        matches = re.findall(":: (.*)[{$]", line)
        return matches[0].strip() if len(matches) == 1 else None

    def parseLink(line):
        # TODO: can have multiple links on same page.
        if not "|" in line:
            matches = re.findall("\[\[(.*)\]\]", line)
            return matches[0] if len(matches) == 1 else None

        tail = l.split("|")[1]
        matches = re.findall("(.*)\]\]", tail)
        return matches[0] if len(matches) == 1 else None

    currentPassage = None
    passages: List[
        Passage
    ] = []  # TODO this code gets much cleaner if this is a dictionary.
    for l in lines:
        newPassage = parsePassage(l)
        if newPassage:
            for p in passages:
                if p.title == newPassage:
                    currentPassage = p
                    break
            else:
                currentPassage = Passage(title=newPassage)
                passages += [currentPassage]
            currentPassage.found_passage = True
            continue

        link = parseLink(l)
        if link:
            # check if passage in all_passages
            # else add it.
            assert currentPassage
            currentLink = None
            for p in passages:
                if p.title == link:
                    currentLink = p
                    break
            else:
                currentLink = Passage(title=link)
                passages += [currentLink]

            currentPassage.outgoing += [currentLink]
            currentLink.incoming += [currentPassage]
            """
            print(
                f"{currentPassage.title}->{currentLink.title}, {len(currentPassage.outgoing)}\n {currentPassage.outgoing}"
            )
            print(
                f"{currentLink.title}<-{currentPassage.title}, {len(currentPassage.incoming)}"
            )
            """
            continue

    return passages


if __name__ == "__main__":
    f = open("../ZachWebSite/wwwroot/games/h.twee")
    validate(f.readlines())
