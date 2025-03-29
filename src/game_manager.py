from tkinter import *
from tkinter import messagebox
from src.graph_manager import *
from src.graph_logic import *
from src.graph_renderer import *
from src.graph_ui import *
from src.audio_manager import *
from src.button_manager import *
from src.led_strip_manager import *


class GameManager:
    """Manage the overall game state, including logic, UI, audio, and hardware interactions."""

    def __init__(self):
        self.score = 0
        self.difficulty = 6

        # Initialize the graph structure and game logic
        self.graph = GraphManager()
        self.logic = GraphLogic(self)

        # Initialize and play background music
        # self.audio_manager = AudioManager()
        # self.audio_manager.play_music("assets/sounds/music_1.wav")

        # Initialize UI components
        self.graph_renderer = GraphRenderer(self)
        self.graph_ui = GraphUI(self)
        self.root = self.graph_ui.root

        # LED Strip
        self.led_strip_manager = LEDStripManager()

        # Start GPIO button verification
        self.running = True
        self.button_manager = ButtonManager([17, 22, 23, 27, 16])  # GPIO pin setup
        self.check_buttons()  # Start monitoring button presses

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
                self.check_path()

            self.root.after(100, self.check_buttons)  # Check every 100ms

    def next_node(self):
        """Move selection to the next available node in a cyclic manner."""
        self.logic.selection_index = (self.logic.selection_index + 1) % len(
            self.logic.available_nodes
        )
        self.graph_renderer.display_user_path()

    def previous_node(self):
        """Move selection to the previous available node in a cyclic manner."""
        self.logic.selection_index = (self.logic.selection_index - 1) % len(
            self.logic.available_nodes
        )
        self.graph_renderer.display_user_path()

    def select_node(self):
        """Handle node selection."""
        self.logic.change_current_node()
        self.graph_renderer.display_user_path()

    def reset_selection(self):
        """Reset all selected nodes and edges."""
        self.logic.reset_selection()
        self.graph_renderer.display_graph()

    def restart_game(self):
        """Restart the game."""
        self.logic.restart_game()
        self.graph_renderer.display_user_path()

    def quit_game(self):
        """Close the application."""
        self.led_strip_manager.clear()
        self.running = False
        self.button_manager.cleanup()
        self.root.quit()

    def on_click(self, event):
        """Handle node clicks and builds the user's selected path"""
        if event.xdata and event.ydata:
            for node, position in self.graph.node_positions.items():
                if (
                    abs(event.xdata - position[0]) < 0.2
                    and abs(event.ydata - position[1]) < 0.2
                ):
                    self.logic.handle_node_click(node)
                    self.graph_renderer.display_user_path()
                    break

    def check_path(self):
        """Check if the user's selected path is the shortest path"""
        result, score = self.logic.check_shortest_path()
        if result.startswith("Congratulations"):
            messagebox.showinfo("Success", result)
            self.restart_game()
        else:
            messagebox.showerror("Error", result)
            self.reset_selection()
        self.led_strip_manager.blink(
            self.led_strip_manager.score_effect(score / 100), 5, 200
        )
        self.led_strip_manager.clear()
        self.score += score * self.difficulty
        self.graph_ui.update_score_display(self.score)

    def toggle_shortest_path(self):
        """Display or hide the shortest path directly on the graph"""
        if not self.logic.shortest_path_displayed:
            path = self.graph.shortest_path(self.logic.start_node, self.logic.end_node)
            if path:
                self.graph_renderer.highlight_shortest_path(path)
            else:
                messagebox.showerror("Error", "No path found.")
        else:
            self.graph_renderer.display_user_path()
        self.logic.shortest_path_displayed = not self.logic.shortest_path_displayed
