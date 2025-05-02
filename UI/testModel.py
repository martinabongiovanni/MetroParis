# Qui testo il modello prima di collegarlo all'interfaccia grafica così da controllare che tutto funzioni
from model.fermata import Fermata
from model.model import Model

# creo un modello
model = Model() # creare il modello mi chiama il costruttore => il grafo esisterà ma sarà vuoto!
# costruisco il grafico
model.buildGraphPesato()
# stampo il numero di nodi e di archi del grafo
print(f"Num nodi: {model.getNumNodi()}")
print(f"Num archi: {model.getNumArchi()}")

f = Fermata(2, "Abbesses", 2.33855, 48.8843)
nodesDFS = model.getBFSNodesFromEdges(f)
for n in nodesDFS:
    print(n)

print("-------------------------------------------------")

archiMaggiori = model.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a)
