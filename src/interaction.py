import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphInterface:
    def __init__(self, root:tk.Tk, graph):
        self.root = root
        self.graph = graph

        self.root.title("DuckQuest - Game Interface")

        # Global styles
        self.root.configure(bg='#282C34')  # Dark background
        self.button_style = {
            'bg': '#61AFEF',
            'fg': 'white',
            'font': ('Arial', 12, 'bold'),
            'relief': tk.RAISED,
            'borderwidth': 2,
            'activebackground': '#528AAE',
        }

        # Container for buttons
        self.button_frame = tk.Frame(self.root, bg='#282C34')
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Buttons
        self.restart_button = tk.Button(
            self.button_frame, text="Start a Graph", command=self.restart_game, **self.button_style
        )
        self.restart_button.pack(fill=tk.X, pady=10)

        self.shortest_path_button = tk.Button(
            self.button_frame, text="Display Shortest Path", command=self.toggle_shortest_path, **self.button_style
        )
        self.shortest_path_button.pack(fill=tk.X, pady=10)

        self.quit_button = tk.Button(
            self.button_frame, text="Quit", command=self.quit_game, **self.button_style
        )
        self.quit_button.pack(fill=tk.X, pady=10)

        # Graph display area
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.shortest_path_displayed = False

        # Initialize the graph
        self.graph.assign_weights_and_colors()
        self.display_graph()

    def quit_game(self):
        """Closes the application"""
        self.root.quit()

    def restart_game(self):
        """Restarts the game by randomizing edge weights"""
        self.graph.assign_weights_and_colors()
        self.shortest_path_displayed = False
        self.display_graph()

    def toggle_shortest_path(self):
        """Displays or hides the shortest path directly on the graph"""
        if not self.shortest_path_displayed:
            # Example with a test path between 'A1' and 'Q2'
            path = self.graph.shortest_path('A1', 'Q2')
            if path:
                self.highlight_shortest_path(path)
            else:
                messagebox.showinfo("Info", "No path found.")
        else:
            self.display_graph()

        self.shortest_path_displayed = not self.shortest_path_displayed

    def highlight_shortest_path(self, path:list):
        """Highlights the shortest path in purple"""
        edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        edge_colors = []
        for edge in self.graph.graph.edges():
            if edge in edges_in_path or (edge[1], edge[0]) in edges_in_path:
                edge_colors.append('purple')
            else:
                edge_colors.append(self.graph.graph[edge[0]][edge[1]].get('color', 'black'))

        self.display_graph(edge_colors)

    def display_graph(self, edge_colors:list=None):
        """Displays the graph in the main window"""
        self.ax.clear()

        if edge_colors is None:
            edge_colors = [data['color'] for u, v, data in self.graph.graph.edges(data=True)]

        nx.draw(
            self.graph.graph, pos=self.graph.node_positions, ax=self.ax, with_labels=True,
            node_size=500, node_color='lightblue', font_size=8, font_color='black', edge_color=edge_colors, width=5
        )

        self.canvas.draw()
