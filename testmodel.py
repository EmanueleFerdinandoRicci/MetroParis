from model.model import Model

model = Model()
model.buildGraph()
print("Numero nodi:", model.get_num_nodi())
print(f"Numero archi: {model.get_num_archi()}")