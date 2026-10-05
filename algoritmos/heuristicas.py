from math import floor, sqrt

from modelos.tipos import TipoHeuristica


def calcular_manhattan(
    linha_atual: int,
    coluna_atual: int,
    linha_objetivo: int,
    coluna_objetivo: int,
) -> int:
    """Estima quantos movimentos ortogonais faltam até o objetivo."""
    distancia_linhas = abs(linha_atual - linha_objetivo)
    distancia_colunas = abs(coluna_atual - coluna_objetivo)

    return (distancia_linhas + distancia_colunas) * 10


def calcular_euclidiana(
    linha_atual: int,
    coluna_atual: int,
    linha_objetivo: int,
    coluna_objetivo: int,
) -> int:
    """Estima a distância em linha reta, arredondada para baixo."""
    distancia_linhas = linha_atual - linha_objetivo
    distancia_colunas = coluna_atual - coluna_objetivo

    distancia = sqrt(
        distancia_linhas ** 2
        + distancia_colunas ** 2
    )
    return floor(distancia * 10)


def calcular_diagonal(
    linha_atual: int,
    coluna_atual: int,
    linha_objetivo: int,
    coluna_objetivo: int,
) -> int:
    """Combina movimentos diagonais de custo 14 e ortogonais de custo 10."""
    distancia_linhas = abs(linha_atual - linha_objetivo)
    distancia_colunas = abs(coluna_atual - coluna_objetivo)
    passos_diagonais = min(distancia_linhas, distancia_colunas)
    passos_ortogonais = (
        max(distancia_linhas, distancia_colunas)
        - passos_diagonais
    )

    return passos_diagonais * 14 + passos_ortogonais * 10


def calcular_heuristica(
    tipo_heuristica: TipoHeuristica,
    linha_atual: int,
    coluna_atual: int,
    linha_objetivo: int,
    coluna_objetivo: int,
) -> int:
    """Encaminha o cálculo para a heurística escolhida."""
    if tipo_heuristica == TipoHeuristica.EUCLIDIANA:
        return calcular_euclidiana(
            linha_atual,
            coluna_atual,
            linha_objetivo,
            coluna_objetivo,
        )

    if tipo_heuristica == TipoHeuristica.DIAGONAL:
        return calcular_diagonal(
            linha_atual,
            coluna_atual,
            linha_objetivo,
            coluna_objetivo,
        )

    return calcular_manhattan(
        linha_atual,
        coluna_atual,
        linha_objetivo,
        coluna_objetivo,
    )
