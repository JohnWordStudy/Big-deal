from flask import Flask, render_template, jsonify, request
from models import MetroNetwork
from simulation import dijkstra_shortest_path

app = Flask(__name__)

network = MetroNetwork.from_json("data/network.json")


@app.route("/")
def index():
    return render_template("index.html", stations=network.stations)


@app.route("/api/graph")
def api_graph():
    return jsonify({
        "stations": network.stations,
        "edges": [
            {"u": e.u, "v": e.v, "travel_time": e.travel_time}
            for e in network.edges
        ]
    })


@app.route("/api/shortest_path")
def api_shortest_path():
    s = request.args.get("source")
    t = request.args.get("target")
    total_time, path = dijkstra_shortest_path(network.graph, s, t)
    return jsonify({"time": total_time, "path": path})


if __name__ == "__main__":
    app.run(debug=True)
