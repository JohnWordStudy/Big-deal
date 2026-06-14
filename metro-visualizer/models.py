import json
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class Edge:
    u: str
    v: str
    travel_time: int  # minutes


@dataclass
class Line:
    name: str
    stops: List[str]
    headway: int  # minutes


class MetroNetwork:
    def __init__(self, stations, edges: List[Edge], lines: List[Line]):
        self.stations = stations
        self.edges = edges
        self.lines = lines
        self.graph = self._build_graph()

    def _build_graph(self) -> Dict[str, List[Tuple[str, int]]]:
        graph: Dict[str, List[Tuple[str, int]]] = {s: [] for s in self.stations}
        for e in self.edges:
            graph[e.u].append((e.v, e.travel_time))
            graph[e.v].append((e.u, e.travel_time))
        return graph

    @classmethod
    def from_json(cls, path: str) -> "MetroNetwork":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        stations = data["stations"]
        edges = [Edge(e["from"], e["to"], e["travel_time"]) for e in data["edges"]]
        lines = [Line(l["name"], l["stops"], l["headway"]) for l in data["lines"]]
        return cls(stations, edges, lines)
