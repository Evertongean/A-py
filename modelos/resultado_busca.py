from dataclasses import dataclass

from modelos.no import No
from modelos.passo_busca import PassoBusca


@dataclass
class ResultadoBusca:
    """Dados públicos produzidos ao final de uma busca."""

    encontrou: bool
    caminho: list[No]
    nos_visitados: list[No]
    custo_total: float
    passos: list[PassoBusca]
    tempo_execucao: float
