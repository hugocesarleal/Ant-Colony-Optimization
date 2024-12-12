import networkx as nx
import matplotlib.pyplot as plt

def plotarGrafo(arestas, melhorCaminho):
    G = nx.Graph()
    G.add_edges_from(arestas)
    pos = nx.spring_layout(G)

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=12, font_weight="bold")

    if melhorCaminho:
        melhorArestas = [(melhorCaminho[i], melhorCaminho[i + 1]) for i in range(len(melhorCaminho) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=melhorArestas, edge_color="red", width=2)

    plt.title("Grafo com o Melhor Caminho Encontrado")
    plt.show()