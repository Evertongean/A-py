import tkinter as tk
from pathlib import Path

from interface.celula import Celula
from modelos.dados_labirinto import DadosLabirinto
from modelos.no import No
from modelos.passo_busca import PassoBusca
from modelos.resultado_busca import ResultadoBusca
from modelos.tipos import ModoEdicao, TipoCelula, TipoPassoBusca


class Grade(tk.Frame):
    """Grade editável que representa o mapa do projeto."""

    LINHAS = 20
    COLUNAS = 30
    TAMANHO_CELULA_MINIMO = 18
    TAMANHO_CELULA_MAXIMO = 32

    def __init__(self, mestre, ao_editar=None):
        super().__init__(mestre, background="#111827", borderwidth=2)

        self.modo_edicao = ModoEdicao.PAREDE
        self.edicao_habilitada = True
        self.ao_editar = ao_editar
        self.celula_inicio = None
        self.celulas_objetivo = []
        self.multiplos_objetivos_habilitados = False
        self.tamanho_celula = self.TAMANHO_CELULA_MINIMO
        # Compatibilidade com trechos que ainda consultam o primeiro objetivo.
        self.celula_objetivo = None

        self.imagem_tom = self._carregar_imagem_personagem(
            "tom.png",
            "Tom",
            "T",
        )
        self.imagem_jerry = self._carregar_imagem_personagem(
            "jerry.png",
            "Jerry",
            "J",
        )
        # As referências ficam na Grade para o Tkinter não descartar as imagens.

        # Matriz que representa visualmente o mapa.
        self.celulas = []
        self._criar_celulas()

    def _obter_caminho_imagem(self, nome_arquivo: str) -> Path:
        pasta_projeto = Path(__file__).resolve().parent.parent
        return pasta_projeto / "recursos" / "imagens" / nome_arquivo

    def _carregar_imagem_personagem(
        self,
        nome_arquivo: str,
        nome_personagem: str,
        letra_fallback: str,
    ):
        """Carrega e reduz uma imagem; a célula usa a letra se houver falha."""
        caminho = self._obter_caminho_imagem(nome_arquivo)

        if not caminho.is_file():
            print(
                f"Imagem do {nome_personagem} não encontrada. "
                f"Usando letra {letra_fallback}."
            )
            return None

        try:
            imagem_original = tk.PhotoImage(file=str(caminho))
            fator_largura = max(1, (imagem_original.width() + 19) // 20)
            fator_altura = max(1, (imagem_original.height() + 15) // 16)
            fator = max(fator_largura, fator_altura)

            if fator > 1:
                return imagem_original.subsample(fator, fator)

            return imagem_original
        except (tk.TclError, OSError):
            print(
                f"Imagem do {nome_personagem} não pôde ser carregada. "
                f"Usando letra {letra_fallback}."
            )
            return None

    def _criar_celulas(self):
        for linha in range(self.LINHAS):
            linha_de_celulas = []
            self.grid_rowconfigure(
                linha,
                minsize=self.tamanho_celula,
                weight=1,
                uniform="linhas_grade",
            )

            for coluna in range(self.COLUNAS):
                if linha == 0:
                    self.grid_columnconfigure(
                        coluna,
                        minsize=self.tamanho_celula,
                        weight=1,
                        uniform="colunas_grade",
                    )

                celula = Celula(
                    self,
                    linha,
                    coluna,
                    self.imagem_tom,
                    self.imagem_jerry,
                )
                celula.grid(row=linha, column=coluna, sticky="nsew")

                # O argumento padrão guarda a célula correta para cada clique.
                celula.bind(
                    "<Button-1>",
                    lambda evento, celula=celula: self.ao_clicar_celula(celula),
                )
                linha_de_celulas.append(celula)

            self.celulas.append(linha_de_celulas)

    def definir_tamanho_celulas(self, tamanho: int):
        """Ajusta a grade visual entre limites adequados para a interface."""
        tamanho_limitado = max(
            self.TAMANHO_CELULA_MINIMO,
            min(self.TAMANHO_CELULA_MAXIMO, tamanho),
        )

        if tamanho_limitado == self.tamanho_celula:
            return

        self.tamanho_celula = tamanho_limitado

        for linha in range(self.LINHAS):
            self.grid_rowconfigure(linha, minsize=tamanho_limitado)

        for coluna in range(self.COLUNAS):
            self.grid_columnconfigure(coluna, minsize=tamanho_limitado)

    def ajustar_ao_espaco(self, largura: int, altura: int, margem: int = 16):
        """Escolhe células quadradas que caibam no espaço disponível."""
        largura_util = max(0, largura - margem)
        altura_util = max(0, altura - margem)
        tamanho_por_largura = largura_util // self.COLUNAS
        tamanho_por_altura = altura_util // self.LINHAS
        tamanho = min(tamanho_por_largura, tamanho_por_altura)
        self.definir_tamanho_celulas(tamanho)

    def definir_modo_edicao(self, modo):
        self.modo_edicao = modo

    def definir_edicao_habilitada(self, habilitada: bool):
        self.edicao_habilitada = habilitada

    def definir_multiplos_objetivos_habilitados(self, habilitados: bool):
        self.multiplos_objetivos_habilitados = habilitados

    def ao_clicar_celula(self, celula):
        """Executa a ação do modo de edição atual na célula clicada."""
        if not self.edicao_habilitada:
            return

        alterou_grade = False

        if self.modo_edicao == ModoEdicao.INICIO:
            alterou_grade = self._posicionar_inicio(celula)
        elif self.modo_edicao == ModoEdicao.OBJETIVO:
            alterou_grade = self._posicionar_objetivo(celula)
        elif self.modo_edicao == ModoEdicao.PAREDE:
            alterou_grade = self._criar_parede(celula)
        elif self.modo_edicao == ModoEdicao.APAGAR:
            alterou_grade = self._apagar_celula(celula)

        if alterou_grade and self.ao_editar is not None:
            self.ao_editar()

    def _posicionar_inicio(self, celula):
        if celula in self.celulas_objetivo:
            return False

        if celula == self.celula_inicio:
            return False

        if self.celula_inicio is not None:
            self.celula_inicio.definir_tipo(TipoCelula.VAZIA)

        celula.definir_tipo(TipoCelula.INICIO)
        self.celula_inicio = celula
        return True

    def _posicionar_objetivo(self, celula):
        if celula == self.celula_inicio:
            return False

        if celula in self.celulas_objetivo:
            return False

        if not self.multiplos_objetivos_habilitados:
            for objetivo_anterior in self.celulas_objetivo:
                objetivo_anterior.definir_tipo(TipoCelula.VAZIA)

            self.celulas_objetivo.clear()

        celula.definir_tipo(TipoCelula.OBJETIVO)
        self.celulas_objetivo.append(celula)
        self._sincronizar_primeiro_objetivo()
        return True

    def _criar_parede(self, celula):
        if celula == self.celula_inicio or celula in self.celulas_objetivo:
            return False

        if celula.tipo == TipoCelula.PAREDE:
            return False

        celula.definir_tipo(TipoCelula.PAREDE)
        return True

    def _apagar_celula(self, celula):
        if celula.tipo == TipoCelula.VAZIA:
            return False

        if celula == self.celula_inicio:
            self.celula_inicio = None

        if celula in self.celulas_objetivo:
            self.celulas_objetivo.remove(celula)
            self._sincronizar_primeiro_objetivo()

        celula.definir_tipo(TipoCelula.VAZIA)
        return True

    def limpar_grade(self):
        for linha_de_celulas in self.celulas:
            for celula in linha_de_celulas:
                celula.definir_tipo(TipoCelula.VAZIA)

        self.celula_inicio = None
        self.celulas_objetivo.clear()
        self.celula_objetivo = None

    def carregar_labirinto(self, dados_labirinto: DadosLabirinto):
        """Substitui o mapa atual pelos dados de um cenário pronto."""
        self._validar_dimensoes_labirinto(dados_labirinto)
        self.limpar_grade()

        for linha in range(self.LINHAS):
            for coluna in range(self.COLUNAS):
                if dados_labirinto.paredes[linha][coluna]:
                    self.celulas[linha][coluna].definir_tipo(
                        TipoCelula.PAREDE
                    )

        self.celula_inicio = self.celulas[
            dados_labirinto.linha_inicio
        ][dados_labirinto.coluna_inicio]
        objetivo = self.celulas[
            dados_labirinto.linha_objetivo
        ][dados_labirinto.coluna_objetivo]
        self.celulas_objetivo.append(objetivo)
        self._sincronizar_primeiro_objetivo()

        self.celula_inicio.definir_tipo(TipoCelula.INICIO)
        self.celula_objetivo.definir_tipo(TipoCelula.OBJETIVO)

    def _sincronizar_primeiro_objetivo(self):
        if self.celulas_objetivo:
            self.celula_objetivo = self.celulas_objetivo[0]
        else:
            self.celula_objetivo = None

    def _validar_dimensoes_labirinto(self, dados_labirinto: DadosLabirinto):
        if len(dados_labirinto.paredes) != self.LINHAS:
            raise ValueError(
                "O labirinto possui uma quantidade inválida de linhas."
            )

        for linha in dados_labirinto.paredes:
            if len(linha) != self.COLUNAS:
                raise ValueError(
                    "O labirinto possui uma quantidade inválida de colunas."
                )

    def limpar_resultado_busca(self):
        """Remove somente as marcações produzidas por uma busca anterior."""
        tipos_de_resultado = (
            TipoCelula.ABERTA,
            TipoCelula.FECHADA,
            TipoCelula.CAMINHO,
        )

        for linha_de_celulas in self.celulas:
            for celula in linha_de_celulas:
                if celula.tipo in tipos_de_resultado:
                    celula.definir_tipo(TipoCelula.VAZIA)
                elif celula.tipo == TipoCelula.OBJETIVO_ALCANCADO:
                    celula.definir_tipo(TipoCelula.OBJETIVO)

    def limpar_exploracao_busca(self):
        """Remove ABERTA e FECHADA, preservando caminhos e objetivos."""
        for linha_de_celulas in self.celulas:
            for celula in linha_de_celulas:
                if celula.tipo in (TipoCelula.ABERTA, TipoCelula.FECHADA):
                    celula.definir_tipo(TipoCelula.VAZIA)

    def marcar_objetivo_alcancado(self, posicao: tuple[int, int]):
        linha, coluna = posicao
        celula = self.celulas[linha][coluna]

        if celula in self.celulas_objetivo:
            celula.definir_tipo(TipoCelula.OBJETIVO_ALCANCADO)

    def mostrar_resultado_busca(self, resultado: ResultadoBusca):
        """Mostra imediatamente os nós explorados e o caminho encontrado."""
        for no in resultado.nos_visitados:
            celula = self.celulas[no.linha][no.coluna]

            if (
                celula != self.celula_inicio
                and celula not in self.celulas_objetivo
            ):
                celula.definir_tipo(TipoCelula.FECHADA)

        # O caminho é desenhado depois para ficar visível sobre os explorados.
        for no in resultado.caminho:
            celula = self.celulas[no.linha][no.coluna]

            if (
                celula != self.celula_inicio
                and celula not in self.celulas_objetivo
            ):
                celula.definir_tipo(TipoCelula.CAMINHO)

    def aplicar_passo_busca(self, passo: PassoBusca):
        """Traduz um evento calculado pelo algoritmo para uma cor na grade."""
        celula = self.celulas[passo.linha][passo.coluna]
        tipos_preservados = (
            TipoCelula.INICIO,
            TipoCelula.OBJETIVO,
            TipoCelula.OBJETIVO_ALCANCADO,
            TipoCelula.PAREDE,
        )

        if celula.tipo in tipos_preservados:
            return

        if passo.tipo == TipoPassoBusca.ABERTO:
            celula.definir_tipo(TipoCelula.ABERTA)
        elif passo.tipo == TipoPassoBusca.FECHADO:
            celula.definir_tipo(TipoCelula.FECHADA)

    def marcar_no_caminho(self, no: No):
        """Marca um nó intermediário do caminho sem cobrir pontos especiais."""
        celula = self.celulas[no.linha][no.coluna]
        tipos_preservados = (
            TipoCelula.INICIO,
            TipoCelula.OBJETIVO,
            TipoCelula.OBJETIVO_ALCANCADO,
            TipoCelula.PAREDE,
        )

        if celula.tipo not in tipos_preservados:
            celula.definir_tipo(TipoCelula.CAMINHO)

    def obter_posicao_inicio(self):
        if self.celula_inicio is None:
            return None

        return (self.celula_inicio.linha, self.celula_inicio.coluna)

    def obter_posicao_objetivo(self):
        """Retorna o primeiro objetivo para preservar compatibilidade."""
        if self.celula_objetivo is None:
            return None

        return (self.celula_objetivo.linha, self.celula_objetivo.coluna)

    def obter_posicoes_objetivo(self) -> list[tuple[int, int]]:
        return [
            (celula.linha, celula.coluna)
            for celula in self.celulas_objetivo
        ]

    def obter_paredes(self):
        """Retorna uma matriz em que True indica a presença de uma parede."""
        paredes = []

        for linha_de_celulas in self.celulas:
            linha_de_paredes = []

            for celula in linha_de_celulas:
                eh_parede = celula.tipo == TipoCelula.PAREDE
                linha_de_paredes.append(eh_parede)

            paredes.append(linha_de_paredes)

        return paredes
