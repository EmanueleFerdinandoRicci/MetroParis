from model.fermata import Fermata
from model.model import Model

model = Model()
model._buildGraphPesato()
print("Numero nodi:", model.get_num_nodi())
print(f"Numero archi: {model.get_num_archi()}")

source = Fermata(2,"Abbesses",2.33855,48.8843)
nodiBFS = model.getBFSNodesFromEdges(source)
for i in range(0,10):
    print(nodiBFS[i])
print("Numero nodi BFS:", len(nodiBFS))
nodiDFS = model.getDFSNodesFromEdges(source)
for i in range(0,10):
    print(nodiDFS[i])
print("Numero nodi DFS:", len(nodiDFS))

print("======================")

print("Archi con peso 2")
archiMaggiori = model.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a[0], "->", a[1], ":", a[2])