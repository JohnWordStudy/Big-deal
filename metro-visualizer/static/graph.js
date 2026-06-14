let graph = null;
let positions = {};

async function loadGraph() {
    const res = await fetch("/api/graph");
    graph = await res.json();

    // 随机给每个站点一个坐标
    graph.stations.forEach(s => {
        positions[s] = {
            x: Math.random() * 700 + 50,
            y: Math.random() * 400 + 50
        };
    });

    draw();
}

function draw(path = []) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 画边
    graph.edges.forEach(e => {
        const p1 = positions[e.u];
        const p2 = positions[e.v];

        ctx.strokeStyle = path.includes(e.u) && path.includes(e.v) ? "red" : "#888";
        ctx.lineWidth = path.includes(e.u) && path.includes(e.v) ? 4 : 2;

        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
    });

    // 画站点
    graph.stations.forEach(s => {
        const p = positions[s];
        ctx.fillStyle = "black";
        ctx.beginPath();
        ctx.arc(p.x, p.y, 8, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillText(s, p.x + 10, p.y + 5);
    });
}

async function findPath() {
    const s = document.getElementById("source").value;
    const t = document.getElementById("target").value;

    const res = await fetch(`/api/shortest_path?source=${s}&target=${t}`);
    const data = await res.json();

    draw(data.path);
}

loadGraph();
