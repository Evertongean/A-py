def converter_nivel_em_atraso(nivel: int) -> int:
    """Converte a velocidade visual em atraso de animação, em milissegundos."""
    atrasos = {
        1: 700,
        2: 550,
        3: 425,
        4: 325,
        5: 250,
        6: 200,
        7: 150,
        8: 100,
        9: 70,
        10: 40,
    }
    return atrasos[nivel]
