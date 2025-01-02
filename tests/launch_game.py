# Import tkinter for creating the GUI
import tkinter as tk

# Import system and OS modules to modify the Python import path
import sys
import os

# Add the 'src' directory to the Python path to enable custom imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

# Import custom modules for graph and interaction logic
from my_graph import *
from interaction import *

# Initialize the main application window
root = tk.Tk()

# Create the graph and its interface
graph = MyGraph()
interface = GraphInterface(root, graph)
graph.edge_weight('A1', 'B1')
# Start the GUI event loop
root.mainloop()
sys.exit()