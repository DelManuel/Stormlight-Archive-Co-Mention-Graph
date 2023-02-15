#%%
import networkx as nx
import ebooklib
from ebooklib import epub
import pickle
import pandas as pd
#%% To load the character list
with open('character_list.pickle', 'rb') as f:
    character_list = pickle.load(f)


impossible_characters = ["Ten"]

problematic_characters = ['Gift', 'Ki', 'Mem', 'Sani', 'Beard', 'Mill',
                         'Gallant', 'Jost', 'Rock', 'Spark', 'Lin', 'Fin', "Design"]

# "Da" con "Dali" con "Dalinar"
# ROOOOOOOOOOOOCK
# "Lift" y "El" son algunos importantes
# "Av" con Avado
# "Gallant nooooo"
# "Betha" con "Bethab"

# To find characters whose name is problematic

# For characters whose name are inside another character´s name. Ex. "Da" in "Dalinar".
inside_characters = [] 

for character_i in character_list:
    for character_j in character_list:
        if (character_i.lower() in character_j.lower()) and (character_i != character_j) and (character_i not in inside_characters):
            inside_characters.append(character_i)
        
 
#%% To fix the character list
for i, character in enumerate(character_list):
    character_new_name = character 
    
    if ("Kholin" in character) or ("Davar" in character) or ("Sadeas" in character) or ("Roshone" in character):
        count = 0
        while character[count] != "_":
            count += 1
        character_new_name = character[:count]
    
    if ("Brightlord" in character) or ("Sebarial" in character):
        count = 0
        while character[count] != "_":
            count += 1
        character_new_name = character[count+1:]


    # Since the change occurs at the last line, Sadeas will be Sadeas
    if character == "Torol_Sadeas":
        character_new_name = "Sadeas"
    if character == "Toralin_Roshone":
        character_new_name = "Roshone"
    if character == "Sylphrena":
        character_new_name = "Syl"
    character_list[i] = character_new_name
#%%-----------------Setting up the book-----------

wok = epub.read_epub('books/Sanderson, Brandon - The Way of Kings.epub')

items = list(wok.get_items_of_type(ebooklib.ITEM_DOCUMENT))

caps = [10,110] # Items from where WOK prologue starts and the epilogue ends

#%%-------------Looping through the chapters to create the links-------------

G = nx.MultiGraph()

chapter_actual_number = 0
    
for chapter in items[10:110]:
    chapter_content = str(chapter.get_content())
    # We loop through the list of characters
    characters_in_chapter = []


    for character in character_list:

        if character in impossible_characters:
            continue

        # If the character is in the chapter, we add it to the list
        if (character not in inside_characters) and (character not in problematic_characters):
            if character in chapter_content:
                #print(chapter_content[i-40:i+40])
                #print(character)
                characters_in_chapter.append(character)
        
        # For difficult characters
        # There is still a problem because characters like fin appear in the prologue 
        else:
            if character in chapter_content:
                char_str_len = len(character)
                i = 0
                while (i < len(chapter_content)-char_str_len) and (character not in characters_in_chapter):
                    if (character == chapter_content[i:i+char_str_len]) and (chapter_content[i+char_str_len].isalpha() == False) and ((chapter_content[i-1] == " ") or (chapter_content[i-1] == ".")): 
                        print(chapter_content[i:i+char_str_len])
                        print(chapter_content[i-40:i+40])
                        print(character)
                        
                        characters_in_chapter.append(character)
                    i += 1
                
        
    # This means it's an actual chapter
    if len(characters_in_chapter) > 2:
        chapter_actual_number += 1
    i = 0

    # We loop through the characters in the chapter to create the links
    while i < len(characters_in_chapter):
        j = i + 1
        character_i = characters_in_chapter[i]
        while j < len(characters_in_chapter):
            character_j = characters_in_chapter[j]

            G.add_edge(character_i, character_j, chapter = f"{chapter_actual_number}")

            j += 1
        i += 1

    
#%% To save the graph

nx.write_gpickle(G, "Graph.gpickle")
#%% To save the tables to input in Gephi

# To save the nodes 

nodos_nuevos = []
for node in (G.nodes()):
    atributos = [node, node]
    nodos_nuevos.append(atributos)
df1 = pd.DataFrame(nodos_nuevos, columns= ["Id", "Label"])

filename = f"nodes_table2.csv"
df1 = df1.set_index("Id")
df1.to_csv(filename)

# To save the edges
new_edges = []
for edge in (G.edges(data = True)):
    edge_info = [edge[0],edge[1], edge[2]["chapter"]]
    new_edges.append(edge_info)
df2 = pd.DataFrame(new_edges, columns= ["Source", "Target", "Chapter"])
df2 = df2.set_index("Source")

filename = f"edges_table2.csv"
df2.to_csv(filename)

# def chapter_to_str(chapter):
#     soup = BeautifulSoup(chapter.get_body_content(), ‘html.parser’)
#     text = [para.get_text() for para in soup.find_all(‘p’)]
#     return ‘ ‘.join(text)
# texts = {}
# for c in chapters:
# texts[c.get_name()] = chapter_to_str(c)]

#%% Agregamos pesos a los enlaces

def crear_red_pesada(red):

    G_pesada = nx.Graph()
    enlaces_chequeados = []
    lista_enlaces = list(red.edges())
    for i,enlace_i in (enumerate(lista_enlaces)):
        peso_enlace = 1
        if enlace_i not in enlaces_chequeados:
            for j in range(i+1,len(lista_enlaces)):
                enlace_j = lista_enlaces[j]
                if enlace_i == enlace_j:
                    peso_enlace +=1
        
            enlaces_chequeados.append(enlace_i)
            if enlace_i in G_pesada.edges():
                G[enlace_i[0]][enlace_i[1]]["weight"] += 1
            else:  
                G_pesada.add_edge(enlace_i[0],enlace_i[1], weight = peso_enlace)
            
    return G_pesada

