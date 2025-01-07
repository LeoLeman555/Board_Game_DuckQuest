# Import system and OS modules to modify the Python import path
import sys
import os

# Dynamically add the 'src' directory to the Python path to enable custom imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.append(src_path)

# Import the custom MyGraph class from the graph module
from graph_manager import *

def print_graph_info(graph):
    """Function to print basic graph information including nodes, edges, and positions"""
    # Print the nodes in the graph
    print("Nodes in the graph:")
    for node in graph.graph.nodes():
        print(node)

    # Print the edges with weights
    print("\nEdges in the graph with weights:")
    for edge in graph.graph.edges(data=True):
        print(f"Edge {edge[0]} - {edge[1]}: Weight = {edge[2].get('weight')}")

    # Print the predefined node positions
    print("\nNode positions:")
    for node, position in graph.node_positions.items():
        print(f"{node}: {position}")

def print_shortest_path(graph, start, end):
    """Function to print the shortest path between two nodes"""
    path = graph.shortest_path(start, end)
    if path:
        print(f"\nShortest path from {start} to {end}: {path}")
    else:
        print(f"\nNo path found between {start} and {end}.")

if __name__ == "__main__":
    # Create a graph instance
    graph = GraphManager()
    graph.assign_weights_and_colors()

    # Print the basic graph information
    print_graph_info(graph)

    # Print the shortest path from 'A1' to 'Q2'
    print_shortest_path(graph, 'A1', 'Q2')
