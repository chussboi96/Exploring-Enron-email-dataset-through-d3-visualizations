function drag(simulation) {
    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }

    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }

    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }

    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
}

const slider = d3.select("#node-slider");
slider.on("input", function() {
    const numberOfNodes = this.value;
    // Update the graph here based on numberOfNodes
    // This may involve filtering your nodes and updating the force simulation
});

function renderGraph() {
    fetch('http://localhost:5000/data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data.links) || !Array.isArray(data.nodes)) {
                throw new Error('Data is missing links or nodes, or they are not in array format');
            }

            const width = 928;
            const height = 400;

            const svg = d3.select("#graphid").append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("viewBox", [0, 0, width, height])
                .call(d3.zoom().on("zoom", (event) => {
                    svg.attr("transform", event.transform);
                }))
                .append("g");   

            // Define the color scale
            const color = d3.scaleOrdinal(d3.schemeCategory10);

            const links = data.links.map(d => ({...d}));
            const nodes = data.nodes.map(d => ({...d}));

            const simulation = d3.forceSimulation(nodes)
                .force("link", d3.forceLink(links).id(d => d.id))
                .force("charge", d3.forceManyBody())
                .force("center", d3.forceCenter(width / 2, height / 2));

            const link = svg.append("g")
                .attr("stroke", "#999")
                .attr("stroke-opacity", 0.6)
                .selectAll("line")
                .data(links)
                .join("line")
                .attr("stroke-width", d => Math.sqrt(d.value));

            const node = svg.append("g")
                .selectAll("circle")
                .data(nodes)
                .join("circle")
                .attr("r", 5)
                .attr("fill", d => color(d.group)) 
                .call(drag(simulation));

            node.append("title")
                .text(d => d.id);

            simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            });
        })
        .catch(error => {
            console.error('Error processing data:', error);
        });
}

renderGraph();