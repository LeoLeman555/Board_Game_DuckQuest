import random
import networkx as nx

class MyGraph:
    COLORS = [
        (0, 1, 0),        # Soft Green
        (0.78, 1, 0),     # Yellow-Green
        (1, 1, 0),        # Bright Yellow
        (1, 0.5, 0),      # Orange
        (1, 0, 0),        # Bright Red
    ]

    def __init__(self):
        """Initialize the graph with nodes, edges, and positions."""
        self.graph = nx.Graph()
        self.nodes = self._initialize_nodes()
        self.edges = self._initialize_edges()
        self.node_positions = self._initialize_node_positions()

        # Add nodes and edges to the graph
        self.graph.add_nodes_from(self.nodes)
        self.graph.add_edges_from(self.edges)

    def _initialize_nodes(self) -> list[str]:
        """Create the list of graph nodes."""
        return [
            f'{letter}{number}' 
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
            for number in (1, 2) 
            if not (letter > 'R' and number == 2)
        ]

    def _initialize_edges(self) -> list[tuple[str, str]]:
        """Define the edges of the graph."""
        return [
            ('A1', 'B1'), ('A1', 'C1'), ('A1', 'D1'), ('B1', 'C1'), ('B1', 'D1'), ('B1', 'E1'), 
            ('B1', 'F1'), ('C1', 'E1'), ('C1', 'H1'), ('D1', 'G1'), ('E1', 'F1'), ('E1', 'K1'), 
            ('F1', 'L1'), ('F1', 'M1'), ('G1', 'M1'), ('H1', 'I1'), ('I1', 'J1'), ('I1', 'Q1'), 
            ('J1', 'K1'), ('J1', 'P1'), ('K1', 'L1'), ('K1', 'O1'), ('L1', 'N1'), ('M1', 'V1'), 
            ('N1', 'U1'), ('N1', 'W1'), ('O1', 'P1'), ('O1', 'T1'), ('P1', 'R1'), ('P1', 'S1'), 
            ('Q1', 'R1'), ('R1', 'Z1'), ('S1', 'T1'), ('S1', 'Z1'), ('T1', 'U1'), ('T1', 'Y1'), 
            ('U1', 'X1'), ('V1', 'W1'), ('W1', 'D2'), ('X1', 'Y1'), ('X1', 'B2'), ('Y1', 'A2'), 
            ('Z1', 'A2'), ('Z1', 'H2'), ('A2', 'F2'), ('A2', 'G2'), ('B2', 'C2'), ('B2', 'E2'), 
            ('C2', 'D2'), ('C2', 'L2'), ('E2', 'F2'), ('E2', 'K2'), ('F2', 'J2'), ('G2', 'H2'), 
            ('G2', 'J2'), ('H2', 'I2'), ('I2', 'J2'), ('I2', 'P2'), ('J2', 'O2'), ('K2', 'L2'), 
            ('K2', 'M2'), ('K2', 'O2'), ('L2', 'R2'), ('M2', 'N2'), ('M2', 'R2'), ('N2', 'O2'), 
            ('N2', 'Q2'), ('O2', 'P2'), ('O2', 'Q2'), ('P2', 'Q2')
        ]

    def _initialize_node_positions(self) -> dict[str, tuple[float, float]]:
        """Define predefined node positions for visualization."""
        return {
            'A1': (0, 2.5), 'B1': (0.8, 2.5), 'C1': (1.5, 3.5), 'D1': (1, 1.5),
            'E1': (2, 2.5), 'F1': (2.3, 1.5), 'G1': (1.5, 0.5), 'H1': (1.7, 4.6),
            'I1': (2.3, 4.5), 'J1': (3, 3.8), 'K1': (2.9, 2.6), 'L1': (3.3, 1.2),
            'M1': (2.5, 0.6), 'N1': (4, 1), 'O1': (4, 3.2), 'P1': (3.9, 4.1),
            'Q1': (3.3, 5), 'R1': (4.5, 4.8), 'S1': (5.3, 4.1), 'T1': (4.7, 2.5),
            'U1': (4.7, 1.6), 'V1': (3.8, 0), 'W1': (4.8, 0.3), 'X1': (5.5, 2),
            'Y1': (5.5, 3), 'Z1': (6, 4.7), 'A2': (6.2, 3), 'B2': (6.1, 1.5),
            'C2': (6.1, 0.7), 'D2': (5.7, 0), 'E2': (7, 2), 'F2': (7, 2.7),
            'G2': (7.3, 4), 'H2': (7.5, 4.8), 'I2': (8.5, 4.3), 'J2': (7.6, 3),
            'K2': (7.5, 1.5), 'L2': (7.1, 0.1), 'M2': (8, 1), 'N2': (8.5, 1.3),
            'O2': (8.5, 2.5), 'P2': (8.5, 3.2), 'Q2': (10, 2.5), 'R2': (8, 0.5)
        }

    def assign_weights_and_colors(self, min_weight: int = 1, max_weight: int = 5) -> None:
        """Assign random weights and colors to all edges."""
        if min_weight > max_weight:
            raise ValueError("min_weight must be less than or equal to max_weight.")
        
        for edge in self.graph.edges():
            weight = random.randint(min_weight, max_weight)
            self.graph[edge[0]][edge[1]]['weight'] = weight
            self.graph[edge[0]][edge[1]]['color'] = self.COLORS[weight - 1]

    def shortest_path(self, start: str, end: str) -> list[str] | None:
        """Return the shortest path between two nodes."""
        try:
            return nx.shortest_path(self.graph, source=start, target=end, weight='weight')
        except nx.NetworkXNoPath:
            return None

    def edge_weight(self, node1: str, node2: str) -> int | None:
        """Return the weight of the edge between two nodes."""
        if not self.graph.has_edge(node1, node2):
            return None
        return self.graph[node1][node2].get('weight')

    def neighbors(self, node: str) -> list[str]:
        """Return the neighbors of a node."""
        if node not in self.graph:
            raise ValueError(f"Node '{node}' does not exist in the graph.")
        return list(self.graph.neighbors(node))
