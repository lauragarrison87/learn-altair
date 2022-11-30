# code from https://infovis.fh-potsdam.de/tutorials/infovis7networks.html 
# if doing network, need to run (if you don't already have)
# python3 -m pip install networkx nx_altair

import altair as alt
import networkx as nx
import nx_altair as nxa

import requests
import json

# create a random graph
G_ran = nx.fast_gnp_random_graph(n=50, p=.1)

# draw graph with nx_altair
nxa.draw_networkx(G_ran)#.show()

###########################################################
# show connections in Les Mis
url = "http://bost.ocks.org/mike/miserables/miserables.json"

lesmis = json.loads(requests.get(url).text)

# we specify that the dataset is not a multigraph, there are no self-loops
# or multiedges, multiple edges between nodes
G = nx.readwrite.json_graph.node_link_graph(lesmis, multigraph=False)
print(nx.info(G)) # print how many nodes and how many edges are in graph

# find connectedness of nodes
degrees = dict(G.degree(G.nodes()))

# save the degrees as a node attribute
nx.set_node_attributes(G, degrees, 'degree')
pos = nx.spring_layout(G) # spring layout is default, but nx has other options (https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout)

nxa.draw_networkx(
    G, 
    pos, 
    # width='value:Q',
    node_size='degree:Q',
    node_color='group:N',
    cmap = "category10", # pass colormap that is used
    node_tooltip='name:N',
    linewidths=0, # remove borders from circles
).properties(
    width = 600, 
    height = 500,
).configure_view(
    strokeWidth=0
).save('./basic_charts_html_output/network.html')