from models import MetroNetwork
from simulation import generate_timetable, print_timetable, print_shortest_path


def main():
    network = MetroNetwork.from_json("data/network.json")

    print("Loaded stations:", network.stations)
    print("Lines:")
    for line in network.lines:
        print(f"  {line.name}: {' - '.join(line.stops)}, headway={line.headway} min")

    # 1. 生成简易运行图
    trips = generate_timetable(network, horizon=60)
    print_timetable(trips, limit=30)

    # 2. 计算两站之间的最短运行时间（不考虑等车，只看行车时间）
    print_shortest_path(network, source="A", target="F")

    # 你可以在这里加交互，比如输入起终点
    while True:
        cmd = input("\n输入起点和终点（例如 A F），或 q 退出：").strip()
        if cmd.lower() == "q":
            break
        parts = cmd.split()
        if len(parts) != 2:
            print("格式错误，请重新输入，例如：A F")
            continue
        s, t = parts
        if s not in network.stations or t not in network.stations:
            print("站点不存在，请重新输入。")
            continue
        print_shortest_path(network, s, t)


if __name__ == "__main__":
    main()
