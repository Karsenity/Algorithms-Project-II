import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


m = np.array([
    [0, 1, 1],
    [5, 0, 0],
    [0, 0, 0]
])

g = nx.convert_matrix.from_numpy_array(m, create_using=nx.DiGraph)
nx.draw(g)
plt.show()
