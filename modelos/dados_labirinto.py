from dataclasses import dataclass


@dataclass
class DadosLabirinto:
    """Dados necessários para representar um labirinto na grade."""

    paredes: list[list[bool]]
    linha_inicio: int
    coluna_inicio: int
    linha_objetivo: int
    coluna_objetivo: int
    nome: str = ""
    descricao: str = ""
