from modelos.dados_labirinto import DadosLabirinto
from modelos.tipos import TipoLabirinto


class FabricaLabirintos:
    """Constrói os dados dos cenários prontos de forma didática."""

    @classmethod
    def criar_labirinto(
        cls,
        tipo_labirinto: TipoLabirinto,
        linhas: int,
        colunas: int,
    ) -> DadosLabirinto:
        if tipo_labirinto == TipoLabirinto.COZINHA:
            return cls.criar_cozinha(linhas, colunas)

        if tipo_labirinto == TipoLabirinto.SALA:
            return cls.criar_sala(linhas, colunas)

        if tipo_labirinto == TipoLabirinto.PORAO:
            return cls.criar_porao(linhas, colunas)

        raise ValueError("O modo Manual não possui um labirinto predefinido.")

    @staticmethod
    def obter_nome(tipo_labirinto: TipoLabirinto) -> str:
        nomes = {
            TipoLabirinto.MANUAL: "Manual",
            TipoLabirinto.COZINHA: "Cozinha",
            TipoLabirinto.SALA: "Sala",
            TipoLabirinto.PORAO: "Porão",
        }
        return nomes[tipo_labirinto]

    @staticmethod
    def obter_descricao(tipo_labirinto: TipoLabirinto) -> str:
        descricoes = {
            TipoLabirinto.MANUAL: "Crie seu próprio labirinto.",
            TipoLabirinto.COZINHA: (
                "Dificuldade: Fácil — poucos obstáculos. "
                "Ideal para observar a busca."
            ),
            TipoLabirinto.SALA: (
                "Dificuldade: Média — corredores e diferentes opções de rota."
            ),
            TipoLabirinto.PORAO: (
                "Dificuldade: Difícil — becos e rotas enganosas."
            ),
        }
        return descricoes[tipo_labirinto]

    @classmethod
    def criar_cozinha(cls, linhas: int, colunas: int) -> DadosLabirinto:
        paredes = cls._criar_matriz(linhas, colunas, False)

        # Bancada vertical com uma passagem central.
        #                              coluna 6, linha 0 ate linha 9
        cls._adicionar_parede_vertical(paredes, 6, 0, 9)
        cls._abrir_posicao(paredes, 5, 6)

        # Balcão horizontal com uma passagem próxima ao lado direito.
        cls._adicionar_parede_horizontal(paredes, 10, 6, 17)
        cls._abrir_posicao(paredes, 10, 14)

        # Mesa e armário representados por pequenos blocos.
        cls._adicionar_retangulo(paredes, 3, 11, 5, 13)
        cls._adicionar_retangulo(paredes, 11, 2, 13, 4)

        return DadosLabirinto(
            paredes=paredes,
            linha_inicio=2,
            coluna_inicio=2,
            linha_objetivo=linhas - 3,
            coluna_objetivo=colunas - 4,
            nome=cls.obter_nome(TipoLabirinto.COZINHA),
            descricao=cls.obter_descricao(TipoLabirinto.COZINHA),
        )

    @classmethod
    def criar_sala(cls, linhas: int, colunas: int) -> DadosLabirinto:
        paredes = cls._criar_matriz(linhas, colunas, False)

        # Divisórias alternadas formam corredores e rotas diferentes.
        cls._adicionar_parede_vertical(paredes, 4, 0, 11)
        cls._abrir_posicao(paredes, 3, 4)
        cls._abrir_posicao(paredes, 9, 4)

        cls._adicionar_parede_vertical(paredes, 8, 3, linhas - 1)
        cls._abrir_posicao(paredes, 5, 8)
        cls._abrir_posicao(paredes, 12, 8)

        cls._adicionar_parede_vertical(paredes, 12, 0, 11)
        cls._abrir_posicao(paredes, 2, 12)
        cls._abrir_posicao(paredes, 9, 12)

        cls._adicionar_parede_vertical(paredes, 16, 3, linhas - 1)
        cls._abrir_posicao(paredes, 6, 16)
        cls._abrir_posicao(paredes, 13, 16)

        # Sofás e móveis criam becos curtos entre as divisórias.
        cls._adicionar_parede_horizontal(paredes, 7, 5, 7)
        cls._adicionar_parede_horizontal(paredes, 11, 9, 11)
        cls._adicionar_parede_horizontal(paredes, 5, 13, 15)
        cls._adicionar_retangulo(paredes, 10, 17, 11, 18)

        return DadosLabirinto(
            paredes=paredes,
            linha_inicio=1,
            coluna_inicio=1,
            linha_objetivo=linhas - 2,
            coluna_objetivo=colunas - 2,
            nome=cls.obter_nome(TipoLabirinto.SALA),
            descricao=cls.obter_descricao(TipoLabirinto.SALA),
        )

    @classmethod
    def criar_porao(cls, linhas: int, colunas: int) -> DadosLabirinto:
        paredes = cls._criar_matriz(linhas, colunas, True)
        linha_central = linhas // 2
        linha_superior = 1
        linha_inferior = linhas - 3
        coluna_inicio = 1
        coluna_objetivo = colunas - 2
        coluna_retorno = colunas - 5

        # Rota longa: aproxima-se rapidamente de Jerry e atrai o Guloso.
        cls._abrir_corredor_horizontal(
            paredes,
            linha_central,
            coluna_inicio,
            coluna_retorno,
        )
        cls._abrir_corredor_vertical(
            paredes,
            coluna_retorno,
            linha_superior,
            linha_central,
        )
        cls._abrir_corredor_horizontal(
            paredes,
            linha_superior,
            coluna_retorno,
            coluna_objetivo,
        )
        cls._abrir_corredor_vertical(
            paredes,
            coluna_objetivo,
            linha_superior,
            linha_central,
        )

        # Rota curta: começa afastando-se de Jerry pelo corredor inferior.
        cls._abrir_corredor_vertical(
            paredes,
            coluna_inicio,
            linha_central,
            linha_inferior,
        )
        cls._abrir_corredor_horizontal(
            paredes,
            linha_inferior,
            coluna_inicio,
            coluna_objetivo,
        )
        cls._abrir_corredor_vertical(
            paredes,
            coluna_objetivo,
            linha_central,
            linha_inferior,
        )

        # Corredores sem saída tornam a exploração menos óbvia.
        cls._abrir_corredor_vertical(paredes, 6, 4, linha_central)
        cls._abrir_corredor_horizontal(paredes, 4, 3, 6)
        cls._abrir_corredor_vertical(paredes, 11, linha_central, 10)
        cls._abrir_corredor_horizontal(paredes, 10, 11, 14)
        cls._abrir_corredor_vertical(paredes, 5, 10, linha_inferior)
        cls._abrir_corredor_vertical(paredes, 16, 10, linha_inferior)

        return DadosLabirinto(
            paredes=paredes,
            linha_inicio=linha_central,
            coluna_inicio=coluna_inicio,
            linha_objetivo=linha_central,
            coluna_objetivo=coluna_objetivo,
            nome=cls.obter_nome(TipoLabirinto.PORAO),
            descricao=cls.obter_descricao(TipoLabirinto.PORAO),
        )

    @staticmethod
    def _criar_matriz(
        linhas: int,
        colunas: int,
        valor_inicial: bool,
    ) -> list[list[bool]]:
        matriz = []

        for _ in range(linhas):
            linha = []

            for _ in range(colunas):
                linha.append(valor_inicial)

            matriz.append(linha)

        return matriz

    @staticmethod
    def _adicionar_parede_horizontal(
        paredes: list[list[bool]],
        linha: int,
        coluna_inicial: int,
        coluna_final: int,
    ):
        for coluna in range(coluna_inicial, coluna_final + 1):
            paredes[linha][coluna] = True

    @staticmethod
    def _adicionar_parede_vertical(
        paredes: list[list[bool]],
        coluna: int,
        linha_inicial: int,
        linha_final: int,
    ):
        for linha in range(linha_inicial, linha_final + 1):
            paredes[linha][coluna] = True

    @classmethod
    def _adicionar_retangulo(
        cls,
        paredes: list[list[bool]],
        linha_inicial: int,
        coluna_inicial: int,
        linha_final: int,
        coluna_final: int,
    ):
        for linha in range(linha_inicial, linha_final + 1):
            cls._adicionar_parede_horizontal(
                paredes,
                linha,
                coluna_inicial,
                coluna_final,
            )

    @staticmethod
    def _abrir_posicao(
        paredes: list[list[bool]],
        linha: int,
        coluna: int,
    ):
        paredes[linha][coluna] = False

    @classmethod
    def _abrir_corredor_horizontal(
        cls,
        paredes: list[list[bool]],
        linha: int,
        coluna_inicial: int,
        coluna_final: int,
    ):
        for coluna in range(coluna_inicial, coluna_final + 1):
            cls._abrir_posicao(paredes, linha, coluna)

    @classmethod
    def _abrir_corredor_vertical(
        cls,
        paredes: list[list[bool]],
        coluna: int,
        linha_inicial: int,
        linha_final: int,
    ):
        for linha in range(linha_inicial, linha_final + 1):
            cls._abrir_posicao(paredes, linha, coluna)
