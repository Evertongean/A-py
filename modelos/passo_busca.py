from dataclasses import dataclass

from modelos.tipos import TipoPassoBusca


@dataclass(frozen=True)
class PassoBusca:
    """Fotografia imutável de um nó em um instante da busca."""

    linha: int
    coluna: int
    custo_g: float
    heuristica_h: float
    custo_f: float
    tipo: TipoPassoBusca
    pai_linha: int | None = None
    pai_coluna: int | None = None
