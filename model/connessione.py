from dataclasses import dataclass

@dataclass
class Connessione:
    id_connessione: int
    id_linea : int
    id_stazP: int
    id_stazA: int


    def __hash__(self):
        return self.id_connessione

    def __str__(self):
        return f"{self.id_connessione} - {self.id_linea} : {self.id_stazP} - {self.id_stazA}"

    def __eq__(self, other):
        return self.id_connessione == other.id_connessione
