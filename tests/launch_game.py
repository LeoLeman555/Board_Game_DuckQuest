import os
import sys
import tkinter as tk

# Add the 'src' directory to the Python path to enable custom imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(src_path)

# Import custom modules for graph and interaction logic
from graph_manager import *
from graph_logic import *
from graph_ui import *

# Initialize the main application window
root = tk.Tk()

# Create the graph, its logic and create the user interface
graph = GraphManager()
logic = GraphLogic(graph)
interface = GraphUI(root, logic)

# Start the GUI event loop
root.mainloop()
sys.exit()
