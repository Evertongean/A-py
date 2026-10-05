from __future__ import annotations

from dataclasses import dataclass


@dataclass
class No:
    """Representa uma posição considerada durante a busca."""

    linha: int
    coluna: int

    # G: custo real acumulado desde Tom até este nó.
    custo_g: float

    # H: estimativa do custo restante deste nó até Jerry.
    heuristica_h: float
    pai: No | None

    @property
    def custo_f(self) -> float:
        """F é a soma do custo percorrido com a estimativa restante."""
        return self.custo_g + self.heuristica_h
