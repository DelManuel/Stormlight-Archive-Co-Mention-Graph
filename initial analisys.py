#%%
import networkx as nx
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
plt.style.use("seaborn")
#%% To load the graphs
with open('graphs/WoK.gpickle', 'rb') as f:
    G_wok = pickle.load(f)
with open('graphs/WoR.gpickle', 'rb') as f:
    G_wor = pickle.load(f)
with open('graphs/OB.gpickle', 'rb') as f:
    G_ob = pickle.load(f)
with open('graphs/RoW.gpickle', 'rb') as f:
    G_row = pickle.load(f)



#%% Studying Kaladin´s links

G_wok_simple = nx.Graph(G_wok)
G_wor_simple = nx.Graph(G_wor)
G_ob_simple = nx.Graph(G_ob)
G_row_simple = nx.Graph(G_row)

list_of_graphs = [G_wok_simple, G_wor_simple, G_ob_simple, G_row_simple]

characters_to_analyze = ["Kaladin", "Shallan", "Dalinar", "Venli", "Szeth"]

edges_with_characters_by_book = [[0,0,0,0] for i in characters_to_analyze]

for i, graph in enumerate(list_of_graphs):
    for edge in graph.edges():
        for character in characters_to_analyze:
            if character in edge:
                character_index = characters_to_analyze.index(character)
                edges_with_characters_by_book[character_index][i] += 1

    for j, value in enumerate(edges_with_characters_by_book):
        edges_with_characters_by_book[j][i] /= len(graph.nodes())

#%%
fig, ax = plt.subplots(figsize = (12,8))
for i, character_percentage in enumerate(edges_with_characters_by_book):
    ax.plot(range(1,5),character_percentage, ls = "--", marker = ".", ms = 12, label = characters_to_analyze[i])
ax.grid(True)
ax.legend(fontsize = 16)
ax.set_ylim(-0.05,1)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_xlabel("Book number", fontsize = 18)
ax.set_ylabel("Percentage of characters connected with", fontsize = 18)
ax.tick_params(axis='both', which='major', labelsize=14)
# %%
