#%%
import networkx as nx
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

plt.style.use("default")
plt.style.use("seaborn-dark")
#%% To load the graphs
with open('graphs/WoK.gpickle', 'rb') as f:
    G_wok = pickle.load(f)
with open('graphs/WoR.gpickle', 'rb') as f:
    G_wor = pickle.load(f)
with open('graphs/OB.gpickle', 'rb') as f:
    G_ob = pickle.load(f)
with open('graphs/RoW.gpickle', 'rb') as f:
    G_row = pickle.load(f)


list_of_graphs = [G_wok, G_wor, G_ob, G_row]
#%% Studying central characters´s links

G_wok_simple = nx.Graph(G_wok)
G_wor_simple = nx.Graph(G_wor)
G_ob_simple = nx.Graph(G_ob)
G_row_simple = nx.Graph(G_row)

list_of_simple_graphs = [nx.Graph(G) for G in list_of_graphs]

characters_to_analyze = ["Kaladin", "Shallan", "Dalinar", "Venli", "Szeth", "Stormfather"]

edges_with_characters_by_book = [[0,0,0,0] for i in characters_to_analyze]

for i, graph in enumerate(list_of_simple_graphs):
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
ax.set_ylim(-0.08,1)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_xlabel("Book number", fontsize = 18)
ax.set_ylabel("Percentage of characters connected with", fontsize = 18)
ax.tick_params(axis='both', which='major', labelsize=14)

#plt.savefig("plots/Percentage of characters interacted.png")
#%% Function to pass from MultiGraph to WeightedGraph

def convert_to_weighted(graph):

    G_weighted = nx.Graph()
    checked_edges = []
    edge_list = list(graph.edges())
    for i,edge_i in (enumerate(edge_list)):
        edge_weight = 1
        if edge_i not in checked_edges:
            for j in range(i+1,len(edge_list)):
                enlace_j = edge_list[j]
                if edge_i == enlace_j:
                    edge_weight +=1
        
            checked_edges.append(edge_i)
            if edge_i in G_weighted.edges():
                G_weighted[edge_i[0]][edge_i[1]]["weight"] += 1
            else:  
                G_weighted.add_edge(edge_i[0],edge_i[1], weight = edge_weight)
            
    return G_weighted
#%%

weighted_graphs = [convert_to_weighted(G) for G in list_of_graphs]


# %%

most_interacted = [["",0] for i in range(len(list_of_graphs))] 

for i, G in enumerate(weighted_graphs):

    kaladin_list = dict(G["Kaladin"])
    
    for character, weight in kaladin_list.items():
        weight = weight["weight"]
        if weight > most_interacted[i][1]:
            most_interacted[i] = [character,weight]

most_interacted = {i[0]:i[1] for i in most_interacted}
df = pd.DataFrame(most_interacted, index = ["Characters"])
# %%
fig, axs = plt.subplots(figsize = (8,4))

sns.barplot(data = df, ax = axs, orient = "h")
axs.set_title("Characters who shared the most chapters with Kaladin", fontsize = 18)
axs.tick_params(axis = "both", labelsize = 12)
axs.set_xlabel("Amount of shared chapters",fontsize = 14)

plt.savefig("plots/Characters who shared the most chapters with Kaladin.png")
# %%
