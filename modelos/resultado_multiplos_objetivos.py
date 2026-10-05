from dataclasses import dataclass

from modelos.no import No
from modelos.resultado_busca import ResultadoBusca


@dataclass
class ResultadoMultiplosObjetivos:
    """Resultado acumulado de uma sequência de buscas parciais."""

    encontrou_todos: bool
    caminho_completo: list[No]
    resultados_parciais: list[ResultadoBusca]
    custo_total: float
    nos_explorados_total: int
    tempo_execucao_total: float
    ordem_objetivos: list[tuple[int, int]]
