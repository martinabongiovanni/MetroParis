from dataclasses import dataclass


@ dataclass
class Connessione:
    id_connessione: int
    id_linea: int
    id_stazP: int
    id_stazA: int

    def __hash__(self):
        # delego la mia funzione di hash alla funzione di hash dell'intero che definisce id_connessione
        return hash(self.id_connessione)

    def __eq__(self, other):
        return self.id_connessione == other.id_connessione