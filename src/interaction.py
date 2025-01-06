import json
import tkinter as tk
import networkx as nx
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphInterface:
    def __init__(self, root: tk.Tk, graph):
        self.root = root
        self.graph = graph

        self.root.title("DuckQuest - Game Modelling")
        self.root.configure(bg='#282C34')  # Dark background

        # Styles
        self.button_style = {
            'bg': '#61AFEF',
            'fg': 'white',
            'font': ('Arial', 12, 'bold'),
            'relief': tk.RAISED,
            'borderwidth': 2,
            'activebackground': '#528AAE',
        }

        # Button commands
        button_commands = [
            ("Help", self.help_screen),
            ("Start a graph", self.restart_game),
            ("Reset selection", self.reset_selection),
            ("Check your path", self.check_shortest_path),
            ("Display shortest path", self.toggle_shortest_path),
            ("Quit", self.quit_game),
        ]

        # Container for buttons
        self.button_frame = tk.Frame(self.root, bg='#282C34')
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Generate buttons dynamically
        for text, command in button_commands:
            button = tk.Button(self.button_frame, text=text, command=command, **self.button_style)
            button.pack(fill=tk.X, pady=10)

        # Graph display area
        self.figure, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.shortest_path_displayed = False

        # Variables for user selection
        self.selected_path = []
        self.user_path_edges = []
        self.selected_nodes = set()

        # Initialize the graph
        self.start_node = 'A1'
        self.end_node = 'Q2'
        self.graph.assign_weights_and_colors()
        self.display_graph()
        self.help_screen()

        # Connect click event
        self.canvas.mpl_connect("button_press_event", self.on_click)

    def quit_game(self):
        """Closes the application"""
        self.root.quit()

    def reset_selection(self):
        """Reset all selected nodes and edges"""
        self.selected_path = []
        self.user_path_edges = []
        self.selected_nodes = set()
        self.display_graph()

    def restart_game(self):
        """Restarts the game by randomizing edge weights"""
        self.graph.assign_weights_and_colors()
        self.shortest_path_displayed = False
        self.selected_path = []
        self.user_path_edges = []
        self.selected_nodes = set()
        self.display_graph()

    def help_screen(self):
        """Display the game rules in an organized and visually appealing way."""
        # Clear the current axis
        self.ax.clear()
        self.ax.set_facecolor("#282C34")  # Dark background for better visibility
        self.ax.axis("off")  # Hide axes

        # Load rules from JSON
        with open("data/rules.json", "r") as file:
            rules_data = json.load(file)
        rules = rules_data["rules"]

        # Add the rules as text, starting from the top
        y_position = 1.1  # Start near the top
        line_spacing = 0.04  # Space between lines

        for section in rules:
            header = section["header"]
            content = section["content"]

            # Add section header
            self.ax.text(
                0.05, y_position, header, fontsize=12, fontweight='bold', ha='left', va='top',
                transform=self.ax.transAxes, color='black'
            )
            y_position -= line_spacing * 1.5  # Add extra space after the header

            # Add section content
            for line in content:
                self.ax.text(
                    0.07, y_position, line, fontsize=10, ha='left', va='top',
                    transform=self.ax.transAxes, wrap=True, color='black'
                )
                y_position -= line_spacing

            y_position -= line_spacing * 0.5  # Extra spacing after each section

        # Ensure the canvas updates
        self.canvas.draw()

    def toggle_shortest_path(self):
        """Displays or hides the shortest path directly on the graph"""
        if not self.shortest_path_displayed:
            path = self.graph.shortest_path(self.start_node, self.end_node)
            if path:
                self.highlight_shortest_path(path)
            else:
                messagebox.showerror("Error", "No path found.")
        else:
            self.display_user_path()

        self.shortest_path_displayed = not self.shortest_path_displayed

    def highlight_shortest_path(self, path: list):
        """Highlights the shortest path in purple"""
        edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        edge_colors = []
        for edge in self.graph.graph.edges():
            if edge in edges_in_path or (edge[1], edge[0]) in edges_in_path:
                edge_colors.append('purple')
            else:
                edge_colors.append(self.graph.graph[edge[0]][edge[1]].get('color', 'black'))

        self.display_graph(edge_colors)

    def display_graph(self, edge_colors: list = None, node_colors: dict = None):
        """Displays the graph in the main window with a legend for edge weights and colors"""
        self.ax.clear()

        # Determine edge colors if not provided
        if edge_colors is None:
            edge_colors = [data['color'] for _, _, data in self.graph.graph.edges(data=True)]

        # Determine node colors if not provided
        if node_colors is None:
            node_colors = {node: 'lightblue' for node in self.graph.graph.nodes()}

        # Create a list of colors for nodes
        node_colors_list = [node_colors.get(node, 'lightblue') for node in self.graph.graph.nodes()]

        # Draw the graph
        nx.draw(
            self.graph.graph, pos=self.graph.node_positions, ax=self.ax, with_labels=True,
            node_size=500, node_color=node_colors_list, font_size=8, font_color='black',
            edge_color=edge_colors, width=5
        )

        # Add a legend for edge weights and colors
        weight_color_mapping = {
            1: (0, 1, 0),
            2: (0.78, 1, 0),
            3: (1, 1, 0),
            4: (1, 0.5, 0),
            5: (1, 0, 0)
        }
        # Create legend handles
        legend_handles = [
            plt.Line2D([0], [0], color=color, lw=4, label=f'{weight}')
            for weight, color in weight_color_mapping.items()
        ]

        self.ax.legend(
            handles=legend_handles,
            title="Edge Weights",
            loc='lower left',  # Place the legend in the lower-left corner
            ncol=1,  # Single column for compactness
            fontsize=10,
            title_fontsize=12,
            frameon=True  # Optional: Add a border around the legend
        )

        # Redraw the canvas
        self.canvas.draw()

    def check_shortest_path(self):
        """Check if the user's selected path is the shortest path"""
        if len(self.selected_path) < 2:
            messagebox.showwarning("Warning", "Please select a valid path with at least two nodes")
            return

        try:
            shortest_path = self.graph.shortest_path(self.start_node, self.end_node)
        except nx.NetworkXNoPath:
            messagebox.showerror("Error", "No path between selected nodes.")
            return

        if self.selected_path == shortest_path:
            messagebox.showinfo("Congratulation", "You've found the shortest way!")
            self.restart_game()
        else:
            messagebox.showerror("Wrong", "This is not the shortest route. Try again!")

    def on_click(self, event):
        """Handles node clicks and builds the user's selected path"""
        if event.xdata and event.ydata:
            for node, position in self.graph.node_positions.items():
                if (abs(event.xdata - position[0]) < 0.2 and abs(event.ydata - position[1]) < 0.2):
                    self.handle_node_click(node)

    def handle_node_click(self, node: str):
        """Handles a single node click"""
        if node in self.selected_nodes:
            # Deselect node and remove its connections
            self.selected_nodes.remove(node)
            self.selected_path = [n for n in self.selected_path if n != node]
            self.user_path_edges = [
                edge for edge in self.user_path_edges
                if node not in edge
            ]
        else:
            # Add node to selection
            self.selected_nodes.add(node)
            if self.selected_path and self.selected_path[-1] != node:
                edge = (self.selected_path[-1], node)
                if self.graph.graph.has_edge(*edge) or self.graph.graph.has_edge(*edge[::-1]):
                    self.user_path_edges.append(edge)
            self.selected_path.append(node)

        self.display_user_path()

    def display_user_path(self):
        """Highlights the user's selected path and selected nodes"""
        edge_colors = []
        for edge in self.graph.graph.edges():
            if edge in self.user_path_edges or (edge[1], edge[0]) in self.user_path_edges:
                edge_colors.append('cyan')
            else:
                edge_colors.append(self.graph.graph[edge[0]][edge[1]].get('color', 'black'))

        node_colors = {node: 'cyan' if node in self.selected_nodes else 'lightblue' for node in self.graph.graph.nodes()}

        self.display_graph(edge_colors, node_colors)
