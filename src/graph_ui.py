import json
import tkinter as tk
import networkx as nx
from audio_manager import *
from button_manager import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COLORS = {
    1: (0, 1, 0),  # Soft Green
    2: (0.78, 1, 0),  # Yellow-Green
    3: (1, 1, 0),  # Bright Yellow
    4: (1, 0.5, 0),  # Orange
    5: (1, 0, 0),  # Bright Red
}


class GraphUI:
    """Handles the graphical interface for displaying and interacting with the graph."""

    def __init__(self, root: tk.Tk, logic):
        self.root = root
        self.logic = logic
        self.graph = logic.graph

        self.root.title("DuckQuest - Game Modelling")
        self.root.configure(bg="#282C34")

        # Styles
        self.button_style = {
            "bg": "#61AFEF",
            "fg": "white",
            "font": ("Arial", 12, "bold"),
            "relief": tk.RAISED,
            "borderwidth": 2,
            "activebackground": "#528AAE",
        }

        # Button commands
        self.button_commands = [
            ("Help", self.help_screen),
            ("Start a graph", self.restart_game),
            ("Reset selection", self.reset_selection),
            ("Check your path", self.check_shortest_path),
            ("Select node", self.select_node),
            ("Next node", self.next_node),
            ("Previous node", self.previous_node),
            ("Display shortest path", self.toggle_shortest_path),
            ("Music pause", self.play_music),
            ("Quit", self.quit_game),
        ]

        # Play the music
        self.audio_manager = AudioManager()
        self.audio_manager.play_music("assets/sounds/music_1.wav")

        # Container for buttons
        self.button_frame = tk.Frame(self.root, bg="#282C34")
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        for text, command in self.button_commands:
            button = tk.Button(
                self.button_frame, text=text, command=command, **self.button_style
            )
            button.pack(fill=tk.X, pady=10)

        # Graph display area
        self.figure, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )
        self.display_graph()
        self.help_screen()  # Display help screen on startup
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Start GPIO button verification
        self.running = True
        self.button_manager = ButtonManager([17, 22, 23, 27, 16])
        self.check_buttons()

    def check_buttons(self):
        """Check whether a button is pressed and performs the corresponding action."""
        if self.running:
            pressed_button = self.button_manager.get_pressed_button()
            if pressed_button == 17:
                self.select_node()
            elif pressed_button == 22:
                self.next_node()
            elif pressed_button == 23:
                self.previous_node()
            elif pressed_button == 27:
                self.reset_selection()
            elif pressed_button == 16:
                self.check_shortest_path()

            self.root.after(100, self.check_buttons)  # Check every 100ms

    def quit_game(self):
        """Close the application."""
        self.running = False
        self.button_manager.cleanup()
        self.root.quit()

    def next_node(self):
        """Move selection to the next available node in a cyclic manner."""
        self.logic.selection_index = (self.logic.selection_index + 1) % len(
            self.logic.available_nodes
        )
        self.display_user_path()

    def previous_node(self):
        """Move selection to the previous available node in a cyclic manner."""
        self.logic.selection_index = (self.logic.selection_index - 1) % len(
            self.logic.available_nodes
        )
        self.display_user_path()

    def select_node(self):
        """Handle node selection"""
        self.logic.change_current_node()
        self.display_user_path()

    def reset_selection(self):
        """Reset all selected nodes and edges"""
        self.logic.reset_selection()
        self.display_graph()

    def restart_game(self):
        """Restarts the game by randomizing edge weights"""
        self.logic.restart_game()
        self.display_user_path()

    def on_click(self, event):
        """Handles node clicks and builds the user's selected path"""
        if event.xdata and event.ydata:
            for node, position in self.graph.node_positions.items():
                if (
                    abs(event.xdata - position[0]) < 0.2
                    and abs(event.ydata - position[1]) < 0.2
                ):
                    self.logic.handle_node_click(node)
                    self.display_user_path()
                    break

    def play_music(self):
        """Toggle music playback using AudioManager."""
        self.audio_manager.pause_or_resume_music()

    def play_buzzer(self):
        self.audio_manager.play_sound_effect("assets/sounds/buzzer.wav")

    def increase_volume(self):
        self.audio_manager.increase_volume()

    def decrease_volume(self):
        self.audio_manager.decrease_volume()

    def help_screen(self):
        """Display the game rules in an organized and visually appealing way."""
        y_position = 1.1  # Start near the top
        line_spacing = 0.04  # Space between lines
        # Clear the current axis
        self.ax.clear()
        self.ax.set_facecolor("#282C34")  # Dark background for better visibility
        self.ax.axis("off")  # Hide axes
        # Load rules from JSON
        with open("data/rules.json", "r") as file:
            rules_data = json.load(file)
        rules = rules_data["rules"]
        # Add the rules as text, starting from the top
        for section in rules:
            header = section["header"]
            content = section["content"]
            # Add section header
            self.ax.text(
                0.05,
                y_position,
                header,
                fontsize=12,
                fontweight="bold",
                ha="left",
                va="top",
                transform=self.ax.transAxes,
                color="black",
            )
            y_position -= line_spacing * 1.5  # Add extra space after the header
            for line in content:  # Add section content
                self.ax.text(
                    0.07,
                    y_position,
                    line,
                    fontsize=10,
                    ha="left",
                    va="top",
                    transform=self.ax.transAxes,
                    wrap=True,
                    color="black",
                )
                y_position -= line_spacing
            y_position -= line_spacing * 0.5  # Extra spacing after each section
        # Ensure the canvas updates
        self.canvas.draw()

    def check_shortest_path(self):
        """Check if the user's selected path is the shortest path"""
        result = self.logic.check_shortest_path()
        if result.startswith("Congratulations"):
            messagebox.showinfo("Success", result)
            self.restart_game()
        else:
            messagebox.showerror("Error", result)

    def toggle_shortest_path(self):
        """Displays or hides the shortest path directly on the graph"""
        if not self.logic.shortest_path_displayed:
            path = self.graph.shortest_path(self.logic.start_node, self.logic.end_node)
            if path:
                self.highlight_shortest_path(path)
            else:
                messagebox.showerror("Error", "No path found.")
        else:
            self.display_user_path()
        self.logic.shortest_path_displayed = not self.logic.shortest_path_displayed

    def highlight_shortest_path(self, path: list):
        """Highlights the shortest path in purple"""
        edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        edge_colors = []
        for edge in self.graph.graph.edges():
            if edge in edges_in_path or (edge[1], edge[0]) in edges_in_path:
                edge_colors.append("purple")
            else:
                edge_colors.append(
                    self.graph.graph[edge[0]][edge[1]].get("color", "black")
                )
        self.display_graph(edge_colors)

    def display_user_path(self):
        """Highlights the user's selected path and selected nodes"""
        edge_colors = []
        for edge in self.graph.graph.edges():
            if (
                edge in self.logic.user_path_edges
                or (edge[1], edge[0]) in self.logic.user_path_edges
            ):
                edge_colors.append("cyan")
            else:
                edge_colors.append(
                    self.graph.graph[edge[0]][edge[1]].get("color", "black")
                )
        node_colors = {
            node: (
                "yellow"
                if node == self.logic.available_nodes[self.logic.selection_index]
                and node in self.logic.selected_nodes
                else (
                    "green"
                    if node == self.logic.available_nodes[self.logic.selection_index]
                    else "cyan" if node in self.logic.selected_nodes else "lightblue"
                )
            )
            for node in self.graph.graph.nodes()
        }

        self.display_graph(edge_colors, node_colors)

    def display_graph(self, edge_colors: list = None, node_colors: dict = None):
        """Displays the graph in the main window with a legend for edge weights and colors"""
        self.ax.clear()
        # Determine edge colors if not provided
        if edge_colors is None:
            edge_colors = [
                data["color"] for _, _, data in self.graph.graph.edges(data=True)
            ]
        # Determine node colors if not provided
        if node_colors is None:
            node_colors = {node: "lightblue" for node in self.graph.graph.nodes()}
        # Create a list of colors for nodes
        node_colors_list = [
            node_colors.get(node, "lightblue") for node in self.graph.graph.nodes()
        ]
        # Draw the graph
        nx.draw(
            self.graph.graph,
            pos=self.graph.node_positions,
            ax=self.ax,
            with_labels=True,
            node_size=500,
            node_color=node_colors_list,
            font_size=8,
            font_color="black",
            edge_color=edge_colors,
            width=5,
        )
        self.display_legend()
        # Redraw the canvas
        self.canvas.draw()

    def display_legend(self):
        """Add a legend for edge weights and colors"""
        legend_handles = [
            plt.Line2D([0], [0], color=color, lw=4, label=f"{weight}")
            for weight, color in COLORS.items()
        ]
        self.ax.legend(
            handles=legend_handles,
            title="Edge Weights",
            loc="lower left",
            ncol=1,
            fontsize=10,
            title_fontsize=12,
            frameon=True,
        )
