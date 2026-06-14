from typing import Dict, List, Tuple
from dataclasses import dataclass
import heapq
from tabulate import tabulate

from models import MetroNetwork


@dataclass
class TrainTrip:
    line_name: str
    departure_station: str
    arrival_station: str
    departure_time: int  # minute from 0
    arrival_time: int


def dijkstra_shortest_path(
    graph: Dict[str, List[Tuple[str, int]]],
    source: str,
    target: str
) -> Tuple[int, List[str]]:
    """简单 Dijkstra，返回最短时间和路径"""
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0

    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == target:
            break
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if dist[target] == float("inf"):
        return float("inf"), []

    # 回溯路径
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return dist[target], path


def generate_timetable(
    network: MetroNetwork,
    horizon: int = 60
) -> List[TrainTrip]:
    """
    根据 headway 在给定时间范围内生成列车运行计划（非常简化版）
    horizon: 模拟时间长度（分钟）
    """
    trips: List[TrainTrip] = []

    for line in network.lines:
        # 每个 headway 发一班车，从首站到末站
        t = 0
        while t <= horizon:
            # 正向
            cur_time = t
            for i in range(len(line.stops) - 1):
                u = line.stops[i]
                v = line.stops[i + 1]
                travel_time = _get_travel_time(network, u, v)
                if travel_time is None:
                    continue
                trip = TrainTrip(
                    line_name=line.name,
                    departure_station=u,
                    arrival_station=v,
                    departure_time=cur_time,
                    arrival_time=cur_time + travel_time,
                )
                trips.append(trip)
                cur_time += travel_time
            t += line.headway

    return trips


def _get_travel_time(network: MetroNetwork, u: str, v: str):
    for e in network.edges:
        if (e.u == u and e.v == v) or (e.u == v and e.v == u):
            return e.travel_time
    return None


def print_timetable(trips: List[TrainTrip], limit: int = 20):
    trips_sorted = sorted(trips, key=lambda x: (x.departure_time, x.line_name))
    rows = []
    for t in trips_sorted[:limit]:
        rows.append([
            t.line_name,
            t.departure_station,
            t.arrival_station,
            f"{t.departure_time:02d}",
            f"{t.arrival_time:02d}",
        ])
    print("\n=== Sample Timetable (前几条) ===")
    print(tabulate(
        rows,
        headers=["Line", "From", "To", "Dep(min)", "Arr(min)"],
        tablefmt="github"
    ))


def print_shortest_path(network: MetroNetwork, source: str, target: str):
    total_time, path = dijkstra_shortest_path(network.graph, source, target)
    if not path:
        print(f"从 {source} 到 {target} 不可达")
        return
    print("\n=== Shortest Path ===")
    print(" -> ".join(path))
    print(f"Total travel time: {total_time} min")
