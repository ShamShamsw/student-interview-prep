# Beginner Project 23: Network Analysis of Social Graphs

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Graph data structures, centrality metrics, community detection, adjacency representations, and network visualization

---

## Why This Project?

Networks are everywhere—social media friendships, web page links, citation graphs, and supply chains are all graphs at heart. Understanding how to represent, traverse, and measure graphs is a core computer science skill that appears in technical interviews and real-world ML pipelines alike.

This project teaches you a professional graph analysis workflow where you can:

- represent a social graph as an adjacency list or edge list,
- generate synthetic random graphs (Erdős–Rényi or Barabási–Albert style) or load a CSV edge list,
- compute fundamental graph metrics (degree, density, diameter, clustering coefficient),
- calculate node-level centrality scores (degree centrality, betweenness centrality, closeness centrality),
- detect communities using a simple algorithm (e.g., greedy modularity or label propagation),
- visualize the graph with nodes colored by community,
- and save a complete analysis report to JSON for reproducibility.

---

## Separate Repository

You can also access this project in a separate repository:

[Network Analysis of Social Graphs Repository](https://github.com/ShamShamsw/network-analysis-of-social-graphs.git)

---

## What You Will Build

You will build a command-line network analysis tool that:

1. Generates or loads a social graph as an edge list (nodes = people, edges = friendships).
2. Builds an in-memory adjacency list representation from the edge list.
3. Computes global graph metrics: number of nodes, number of edges, graph density, average degree, and diameter.
4. Computes per-node centrality scores: degree centrality, betweenness centrality, and closeness centrality.
5. Ranks nodes by each centrality measure and identifies the top-5 most influential nodes.
6. Detects communities using a modularity-based or label-propagation algorithm.
7. Prints a structured analysis report with global metrics, top influencers, and community breakdown.
8. Saves a visual plot of the network with community-colored nodes to `data/runs/`.
9. Persists a complete JSON summary of the analysis session for reproducibility.

---

## Requirements

- Python 3.11+
- `numpy`
- `networkx`
- `matplotlib`
- `seaborn`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   NETWORK ANALYSIS OF SOCIAL GRAPHS
======================================================================

Configuration:
   Graph type: Barabási-Albert (preferential attachment)
   Nodes: 100
   Edges per new node (m): 3
   Random seed: 42
   Centrality measures: degree, betweenness, closeness
   Community algorithm: greedy modularity

Graph profile:
   Name: Synthetic BA social graph
   Nodes: 100
   Edges: 291
   Density: 0.0588
   Average degree: 5.82
   Is connected: True
   Diameter: 5
   Average clustering coefficient: 0.147

Top-5 Nodes by Degree Centrality:
   Rank  Node   Degree  Centrality
   1     0      24      0.2424
   2     1      19      0.1919
   3     4      16      0.1616
   4     7      14      0.1414
   5     2      13      0.1313

Top-5 Nodes by Betweenness Centrality:
   Rank  Node   Betweenness
   1     0      0.3214
   2     1      0.2187
   3     4      0.1923
   4     7      0.1541
   5     2      0.1388

Top-5 Nodes by Closeness Centrality:
   Rank  Node   Closeness
   1     0      0.5812
   2     1      0.5103
   3     4      0.4897
   4     7      0.4721
   5     2      0.4603

Community Detection (greedy modularity):
   Communities found: 6
   Modularity score: 0.412

   Community 1:  31 nodes  (hub: node 0)
   Community 2:  24 nodes  (hub: node 1)
   Community 3:  17 nodes  (hub: node 4)
   Community 4:  13 nodes  (hub: node 7)
   Community 5:   9 nodes  (hub: node 2)
   Community 6:   6 nodes  (hub: node 9)

Artifacts saved:
   Network plot:      data/runs/social_graph.png
   Analysis summary:  data/runs/analysis_summary.json

Analysis completed in 1.8 seconds.
```

---

## Build Order

Follow this order for clean architecture:

1. `storage.py` — Generate/load graphs, save JSON summaries and plots
2. `models.py` — Define graph config, metric records, and analysis summary
3. `operations.py` — Compute metrics, centrality, and communities
4. `display.py` — Format tables, reports, and headers
5. `main.py` — Orchestrate the full analysis workflow

---

## Step-by-Step Instructions

### Step 1: Implement `storage.py`

Create functions to:
- Generate a synthetic graph (Barabási–Albert or Erdős–Rényi) using `networkx`
- Load an edge list from a CSV file (columns: `source`, `target`)
- Save the analysis JSON summary
- Save the network visualization plot

**Key functions:**
- `generate_graph(graph_type: str, n: int, seed: int) → nx.Graph`
- `load_graph_from_csv(filepath: str) → nx.Graph`
- `save_analysis_summary(filename: str, summary: dict) → None`
- `save_network_plot(filename: str, graph, communities: list) → None`

### Step 2: Implement `models.py`

Define data models and configuration:
- Analysis configuration (graph type, size, seed, centrality measures)
- Per-node centrality record
- Community record (id, member nodes, hub node)
- Complete analysis summary structure

**Key structures:**
- `create_project_config(graph_type, n_nodes, m, seed) → dict`
- `create_node_metrics(node_id, degree, degree_centrality, betweenness, closeness) → dict`
- `create_community_record(community_id, members, hub_node) → dict`
- `create_analysis_summary(config, graph_profile, node_metrics, communities, ...) → dict`

### Step 3: Implement `operations.py`

Build the core analysis pipeline:
- Compute global graph metrics (density, diameter, clustering coefficient)
- Compute per-node centrality using networkx built-ins
- Detect communities using `networkx.algorithms.community`
- Rank nodes by each centrality measure
- Assemble the full analysis summary

**Key functions:**
- `compute_graph_profile(graph) → dict` — global metrics
- `compute_centrality(graph) → dict[int, dict]` — per-node metrics
- `detect_communities(graph) → tuple[list, float]` — (list of node sets, modularity)
- `rank_nodes(node_metrics, by: str, top_k: int) → list`
- `load_graph_profile() → dict` — constructs profile dict for display
- `run_core_flow() → dict` — orchestrates full pipeline

### Step 4: Implement `display.py`

Format output for readability:
- Header banner
- Configuration and graph profile block
- Centrality ranking tables (Rank / Node / Score columns)
- Community breakdown table
- Final summary with artifact paths

**Key functions:**
- `format_header() → str`
- `format_startup_guide(config, profile) → str`
- `format_centrality_table(ranked_nodes, metric_name) → str`
- `format_community_table(communities) → str`
- `format_run_report(summary) → str`

### Step 5: Implement `main.py`

Orchestrate the workflow:
1. Load configuration and generate/load graph
2. Print header and graph profile
3. Compute metrics and detect communities
4. Print all ranking tables and community breakdown
5. Save JSON summary and network plot

---

## Done Criteria

- [ ] The project runs from `main.py` without crashes.
- [ ] A graph with at least 50 nodes is generated or loaded.
- [ ] Degree, betweenness, and closeness centrality are computed for all nodes.
- [ ] Top-5 nodes are displayed for each centrality measure.
- [ ] At least 3 communities are detected and reported.
- [ ] A network visualization PNG is saved to `data/runs/`.
- [ ] A JSON analysis summary is saved to `data/runs/`.
- [ ] Every function has a docstring.
- [ ] Code is organized by concern (models, operations, display, storage).

---

## Stretch Goals

1. Add PageRank centrality alongside degree/betweenness/closeness.
2. Implement a shortest-path query: given two node IDs, print the shortest path and its length.
3. Support directed graphs (DiGraph) and compare in-degree vs. out-degree distributions.
4. Plot degree distribution as a histogram and check for power-law behavior.
5. Load a real-world dataset (e.g., Karate Club, Les Misérables) from `networkx.generators.social`.
6. Animate community detection steps using matplotlib.
7. Export a community membership CSV (node_id, community_id) for downstream use.
   - display.py
   - main.py

## Done Criteria

- The project runs from main.py without crashes.
- Core workflows from the project instructions are implemented.
- Outputs are readable and validated with sample input.
