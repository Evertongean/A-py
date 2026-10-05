from modelos.tipos import TipoMovimento


DIRECOES_4 = [
    (-1, 0),  # cima
    (1, 0),  # baixo
    (0, -1),  # esquerda
    (0, 1),  # direita
]

DIRECOES_8 = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]


def obter_direcoes(tipo_movimento: TipoMovimento) -> list[tuple[int, int]]:
    """Retorna as direções permitidas pela configuração escolhida."""
    if tipo_movimento == TipoMovimento.OITO_DIRECOES:
        return DIRECOES_8

    return DIRECOES_4


def calcular_custo_movimento(
    diferenca_linha: int,
    diferenca_coluna: int,
) -> int:
    """Retorna 14 para um passo diagonal e 10 para um passo ortogonal."""
    movimento_diagonal = (
        diferenca_linha != 0
        and diferenca_coluna != 0
    )

    if movimento_diagonal:
        return 14

    return 10


def corta_canto_de_parede(
    paredes: list[list[bool]],
    linha_atual: int,
    coluna_atual: int,
    diferenca_linha: int,
    diferenca_coluna: int,
) -> bool:
    """Indica se uma diagonal tentaria passar pelo canto de uma parede."""
    movimento_diagonal = (
        diferenca_linha != 0
        and diferenca_coluna != 0
    )

    if not movimento_diagonal:
        return False

    parede_horizontal = paredes[linha_atual][coluna_atual + diferenca_coluna]
    parede_vertical = paredes[linha_atual + diferenca_linha][coluna_atual]

    return parede_horizontal or parede_vertical
