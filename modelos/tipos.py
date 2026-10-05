from enum import Enum, auto


class TipoCelula(Enum):
    """Estados que uma célula da grade pode assumir."""

    VAZIA = auto()
    PAREDE = auto()
    INICIO = auto()
    OBJETIVO = auto()
    OBJETIVO_ALCANCADO = auto()
    ABERTA = auto()
    FECHADA = auto()
    CAMINHO = auto()


class ModoEdicao(Enum):
    """Ação que será executada ao clicar em uma célula."""

    PAREDE = auto()
    INICIO = auto()
    OBJETIVO = auto()
    APAGAR = auto()


class TipoPassoBusca(Enum):
    """Tipo de acontecimento registrado durante a execução da busca."""

    ABERTO = auto()
    FECHADO = auto()


class TipoAlgoritmo(Enum):
    """Algoritmo que será usado para calcular a busca."""

    A_ESTRELA = auto()
    BUSCA_GULOSA = auto()


class TipoHeuristica(Enum):
    """Heurística usada para estimar a distância até o objetivo."""

    MANHATTAN = auto()
    EUCLIDIANA = auto()
    DIAGONAL = auto()


class TipoMovimento(Enum):
    """Conjunto de direções permitidas durante uma busca."""

    QUATRO_DIRECOES = auto()
    OITO_DIRECOES = auto()


class TipoLabirinto(Enum):
    """Cenário manual ou labirinto pronto escolhido pelo usuário."""

    MANUAL = auto()
    COZINHA = auto()
    SALA = auto()
    PORAO = auto()
