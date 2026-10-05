import tkinter as tk

from algoritmos.a_estrela import AEstrela
from algoritmos.busca_gulosa import BuscaGulosa
from interface.controle_velocidade import converter_nivel_em_atraso
from interface.grade import Grade
from modelos.dados_labirinto import DadosLabirinto
from modelos.resultado_busca import ResultadoBusca
from modelos.tipos import TipoHeuristica, TipoMovimento, TipoPassoBusca


class JanelaComparacao(tk.Toplevel):
    """Exibe A* e Busca Gulosa lado a lado sobre o mesmo mapa."""

    COR_FUNDO = "#111827"
    COR_PAINEL = "#1f2937"
    COR_DESTAQUE = "#f59e0b"
    COR_TEXTO = "#f9fafb"

    def __init__(
        self,
        janela_pai,
        paredes: list[list[bool]],
        inicio: tuple[int, int],
        objetivo: tuple[int, int],
        tipo_heuristica: TipoHeuristica,
        tipo_movimento: TipoMovimento,
    ):
        super().__init__(janela_pai)

        self.title("Comparação A* x Busca Gulosa")
        self.geometry("1600x900")
        self.minsize(1280, 720)
        self.configure(background=self.COR_FUNDO)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.transient(janela_pai)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        # A comparação conserva uma fotografia independente do mapa principal.
        self.paredes = [linha[:] for linha in paredes]
        self.inicio = tuple(inicio)
        self.objetivo = tuple(objetivo)
        self.tipo_heuristica = tipo_heuristica
        self.tipo_movimento = tipo_movimento

        self.a_estrela = AEstrela()
        self.busca_gulosa = BuscaGulosa()
        self.resultado_a_estrela = None
        self.resultado_gulosa = None

        self.indice_passo_a_estrela = 0
        self.indice_passo_gulosa = 0
        self.indice_caminho_a_estrela = 1
        self.indice_caminho_gulosa = 1
        self.contador_explorados_a_estrela = 0
        self.contador_explorados_gulosa = 0
        self.a_estrela_finalizou = False
        self.gulosa_finalizou = False

        self.comparacao_em_reproducao = False
        self.comparacao_pausada = False
        self.id_agendamento = None
        self.atraso_animacao = 250

        self.texto_status_geral = tk.StringVar(
            value="Status geral: Aguardando"
        )
        self.texto_nos_a_estrela = tk.StringVar(value="Nós explorados: 0")
        self.texto_custo_a_estrela = tk.StringVar(value="Custo total: -")
        self.texto_tempo_a_estrela = tk.StringVar(value="Tempo: -")
        self.texto_status_a_estrela = tk.StringVar(value="Status: Aguardando")
        self.texto_nos_gulosa = tk.StringVar(value="Nós explorados: 0")
        self.texto_custo_gulosa = tk.StringVar(value="Custo total: -")
        self.texto_tempo_gulosa = tk.StringVar(value="Tempo: -")
        self.texto_status_gulosa = tk.StringVar(value="Status: Aguardando")
        self.texto_menor_custo = tk.StringVar(value="Menor custo: -")
        self.texto_menos_nos = tk.StringVar(value="Menos nós explorados: -")
        self.texto_menor_tempo = tk.StringVar(
            value="Menor tempo de cálculo: -"
        )
        self.valor_velocidade = tk.IntVar(value=5)

        self._criar_cabecalho()
        self._criar_area_grades()
        self._criar_area_controles()
        self._atualizar_estado_botoes()

    def _criar_cabecalho(self):
        cabecalho = tk.Frame(self, background=self.COR_PAINEL, pady=8)
        cabecalho.grid(row=0, column=0, sticky="ew")

        titulo = tk.Label(
            cabecalho,
            text="COMPARAÇÃO DE ALGORITMOS",
            background=self.COR_PAINEL,
            foreground=self.COR_DESTAQUE,
            font=("Arial", 20, "bold"),
        )
        titulo.pack()

        configuracao = tk.Label(
            cabecalho,
            text=(
                f"Heurística: {self._obter_nome_heuristica()}     "
                f"Movimento: {self._obter_nome_movimento()}     "
                "Custos: ortogonal = 10 | diagonal = 14"
            ),
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 10),
            justify="center",
            wraplength=1200,
        )
        configuracao.pack(pady=(5, 0))

        status = tk.Label(
            cabecalho,
            textvariable=self.texto_status_geral,
            background=self.COR_PAINEL,
            foreground="#d1d5db",
            font=("Arial", 10, "bold"),
        )
        status.pack(pady=(5, 0))

    def _criar_area_grades(self):
        area = tk.Frame(self, background=self.COR_FUNDO)
        area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=14,
            pady=10,
        )
        area.grid_rowconfigure(0, weight=1)
        area.grid_columnconfigure(0, weight=1, uniform="comparacao")
        area.grid_columnconfigure(1, weight=1, uniform="comparacao")

        painel_a_estrela = tk.Frame(area, background=self.COR_PAINEL, padx=10)
        painel_a_estrela.grid(row=0, column=0, sticky="nsew")

        painel_gulosa = tk.Frame(area, background=self.COR_PAINEL, padx=10)
        painel_gulosa.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(14, 0),
        )

        self.grade_a_estrela = self._criar_painel_algoritmo(
            painel_a_estrela,
            "A*",
            "Prioridade = F = G + H",
            (
                self.texto_nos_a_estrela,
                self.texto_custo_a_estrela,
                self.texto_tempo_a_estrela,
                self.texto_status_a_estrela,
            ),
        )
        self.grade_gulosa = self._criar_painel_algoritmo(
            painel_gulosa,
            "BUSCA GULOSA",
            "Prioridade = H",
            (
                self.texto_nos_gulosa,
                self.texto_custo_gulosa,
                self.texto_tempo_gulosa,
                self.texto_status_gulosa,
            ),
        )

        self._carregar_mapa_nas_grades()

    def _criar_painel_algoritmo(
        self,
        mestre,
        titulo: str,
        explicacao: str,
        variaveis_metricas: tuple,
    ) -> Grade:
        mestre.grid_rowconfigure(2, weight=1)
        mestre.grid_columnconfigure(0, weight=1)

        rotulo_titulo = tk.Label(
            mestre,
            text=titulo,
            background=self.COR_PAINEL,
            foreground=self.COR_DESTAQUE,
            font=("Arial", 15, "bold"),
        )
        rotulo_titulo.grid(row=0, column=0, pady=(8, 2))

        rotulo_explicacao = tk.Label(
            mestre,
            text=explicacao,
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 9),
        )
        rotulo_explicacao.grid(row=1, column=0, pady=(0, 7))

        area_grade = tk.Frame(mestre, background=self.COR_PAINEL)
        area_grade.grid(row=2, column=0, sticky="nsew")
        area_grade.grid_rowconfigure(0, weight=1)
        area_grade.grid_columnconfigure(0, weight=1)

        grade = Grade(area_grade)
        grade.grid(row=0, column=0)
        grade.definir_edicao_habilitada(False)
        area_grade.bind(
            "<Configure>",
            lambda evento, grade=grade: grade.ajustar_ao_espaco(
                evento.width,
                evento.height,
            ),
        )

        painel_metricas = tk.Frame(
            mestre,
            background="#374151",
            padx=12,
            pady=7,
        )
        painel_metricas.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(9, 9),
        )

        for variavel in variaveis_metricas:
            rotulo = tk.Label(
                painel_metricas,
                textvariable=variavel,
                anchor="w",
                justify="left",
                wraplength=600,
                background="#374151",
                foreground=self.COR_TEXTO,
                font=("Arial", 10),
            )
            rotulo.pack(fill="x", pady=1)

        return grade

    def _carregar_mapa_nas_grades(self):
        dados_a_estrela = self._criar_dados_do_mapa()
        dados_gulosa = self._criar_dados_do_mapa()
        self.grade_a_estrela.carregar_labirinto(dados_a_estrela)
        self.grade_gulosa.carregar_labirinto(dados_gulosa)
        self.grade_a_estrela.definir_edicao_habilitada(False)
        self.grade_gulosa.definir_edicao_habilitada(False)

    def _criar_dados_do_mapa(self) -> DadosLabirinto:
        linha_inicio, coluna_inicio = self.inicio
        linha_objetivo, coluna_objetivo = self.objetivo
        return DadosLabirinto(
            paredes=[linha[:] for linha in self.paredes],
            linha_inicio=linha_inicio,
            coluna_inicio=coluna_inicio,
            linha_objetivo=linha_objetivo,
            coluna_objetivo=coluna_objetivo,
        )

    def _criar_area_controles(self):
        area = tk.Frame(
            self,
            background=self.COR_PAINEL,
            padx=18,
            pady=10,
        )
        area.grid(row=2, column=0, sticky="ew")
        area.grid_columnconfigure(0, weight=1)
        area.grid_columnconfigure(1, weight=1)

        botoes = tk.Frame(area, background=self.COR_PAINEL)
        botoes.grid(row=0, column=0, columnspan=2)

        self.botao_iniciar = self._criar_botao(
            botoes,
            "▶ Iniciar comparação",
            self.iniciar_comparacao,
            "#047857",
        )
        self.botao_pausar = self._criar_botao(
            botoes,
            "⏸ Pausar",
            self.pausar_comparacao,
        )
        self.botao_continuar = self._criar_botao(
            botoes,
            "▶ Continuar",
            self.continuar_comparacao,
        )
        self.botao_proximo = self._criar_botao(
            botoes,
            "⏭ Próximo passo",
            self.executar_um_passo_comparacao,
        )
        self.botao_reiniciar = self._criar_botao(
            botoes,
            "↻ Reiniciar",
            self.reiniciar_comparacao,
            "#b45309",
        )

        velocidade = tk.Frame(area, background=self.COR_PAINEL)
        velocidade.grid(row=1, column=0, sticky="ew", pady=(7, 0))

        rotulo_velocidade = tk.Label(
            velocidade,
            text="Velocidade",
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 9, "bold"),
        )
        rotulo_velocidade.pack(side="left", padx=(0, 8))

        escala = tk.Scale(
            velocidade,
            from_=1,
            to=10,
            orient="horizontal",
            variable=self.valor_velocidade,
            command=self._alterar_velocidade,
            showvalue=True,
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            highlightthickness=0,
            troughcolor="#4b5563",
            length=260,
        )
        escala.pack(side="left")

        resumo = tk.Frame(
            area,
            background="#374151",
            padx=12,
            pady=6,
        )
        resumo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(24, 0),
            pady=(7, 0),
        )

        titulo_resumo = tk.Label(
            resumo,
            text="RESULTADO DA COMPARAÇÃO",
            background="#374151",
            foreground=self.COR_DESTAQUE,
            font=("Arial", 9, "bold"),
        )
        titulo_resumo.pack(anchor="w")

        for variavel in (
            self.texto_menor_custo,
            self.texto_menos_nos,
            self.texto_menor_tempo,
        ):
            rotulo = tk.Label(
                resumo,
                textvariable=variavel,
                anchor="w",
                justify="left",
                wraplength=650,
                background="#374151",
                foreground=self.COR_TEXTO,
                font=("Arial", 9),
            )
            rotulo.pack(fill="x")

    def _criar_botao(self, mestre, texto, comando, cor="#4b5563"):
        botao = tk.Button(
            mestre,
            text=texto,
            command=comando,
            background=cor,
            foreground=self.COR_TEXTO,
            activebackground=self.COR_DESTAQUE,
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
        )
        botao.pack(side="left", padx=3)
        return botao

    def iniciar_comparacao(self):
        if self.comparacao_em_reproducao:
            return

        if self.resultado_a_estrela is not None:
            self.reiniciar_comparacao()

        paredes_a_estrela = [linha[:] for linha in self.paredes]
        paredes_gulosa = [linha[:] for linha in self.paredes]
        self.texto_status_geral.set("Status geral: Calculando resultados...")
        self.update_idletasks()

        self.resultado_a_estrela = self.a_estrela.buscar(
            paredes_a_estrela,
            self.inicio,
            self.objetivo,
            self.tipo_heuristica,
            self.tipo_movimento,
        )
        self.resultado_gulosa = self.busca_gulosa.buscar(
            paredes_gulosa,
            self.inicio,
            self.objetivo,
            self.tipo_heuristica,
            self.tipo_movimento,
        )

        self.texto_tempo_a_estrela.set(
            self._formatar_tempo(self.resultado_a_estrela.tempo_execucao)
        )
        self.texto_tempo_gulosa.set(
            self._formatar_tempo(self.resultado_gulosa.tempo_execucao)
        )
        self.texto_status_a_estrela.set("Status: Executando...")
        self.texto_status_gulosa.set("Status: Executando...")
        self.texto_status_geral.set("Status geral: Comparação em andamento")
        self.comparacao_em_reproducao = True
        self.comparacao_pausada = False
        self._atualizar_estado_botoes()
        self.executar_proximo_passo_comparacao()

    def executar_proximo_passo_comparacao(self):
        self.id_agendamento = None

        if not self.comparacao_em_reproducao or self.comparacao_pausada:
            return

        self._executar_tick_comparacao()

        if self.comparacao_em_reproducao and not self.comparacao_pausada:
            self.id_agendamento = self.after(
                self.atraso_animacao,
                self.executar_proximo_passo_comparacao,
            )

    def _executar_tick_comparacao(self):
        if not self.a_estrela_finalizou:
            (
                self.indice_passo_a_estrela,
                self.indice_caminho_a_estrela,
                self.contador_explorados_a_estrela,
                self.a_estrela_finalizou,
            ) = self._executar_evento_visual(
                self.grade_a_estrela,
                self.resultado_a_estrela,
                self.indice_passo_a_estrela,
                self.indice_caminho_a_estrela,
                self.contador_explorados_a_estrela,
                self.texto_nos_a_estrela,
                self.texto_custo_a_estrela,
                self.texto_status_a_estrela,
            )

        if not self.gulosa_finalizou:
            (
                self.indice_passo_gulosa,
                self.indice_caminho_gulosa,
                self.contador_explorados_gulosa,
                self.gulosa_finalizou,
            ) = self._executar_evento_visual(
                self.grade_gulosa,
                self.resultado_gulosa,
                self.indice_passo_gulosa,
                self.indice_caminho_gulosa,
                self.contador_explorados_gulosa,
                self.texto_nos_gulosa,
                self.texto_custo_gulosa,
                self.texto_status_gulosa,
            )

        if self.a_estrela_finalizou and self.gulosa_finalizou:
            self.finalizar_comparacao()

    def _executar_evento_visual(
        self,
        grade: Grade,
        resultado: ResultadoBusca,
        indice_passo: int,
        indice_caminho: int,
        contador_explorados: int,
        texto_nos,
        texto_custo,
        texto_status,
    ) -> tuple[int, int, int, bool]:
        if indice_passo < len(resultado.passos):
            passo = resultado.passos[indice_passo]
            grade.aplicar_passo_busca(passo)
            indice_passo += 1

            if passo.tipo == TipoPassoBusca.FECHADO:
                contador_explorados += 1
                texto_nos.set(f"Nós explorados: {contador_explorados}")

            if indice_passo == len(resultado.passos) and resultado.encontrou:
                texto_status.set("Status: Reconstruindo caminho")

        else:
            ultimo_indice = len(resultado.caminho) - 1

            if resultado.encontrou and indice_caminho < ultimo_indice:
                no = resultado.caminho[indice_caminho]
                grade.marcar_no_caminho(no)
                indice_caminho += 1

        terminou_passos = indice_passo >= len(resultado.passos)
        ultimo_indice = len(resultado.caminho) - 1
        terminou_caminho = (
            not resultado.encontrou
            or indice_caminho >= ultimo_indice
        )
        finalizou = terminou_passos and terminou_caminho

        if finalizou:
            self._mostrar_resultado_algoritmo(
                resultado,
                texto_custo,
                texto_status,
            )

        return (
            indice_passo,
            indice_caminho,
            contador_explorados,
            finalizou,
        )

    def _mostrar_resultado_algoritmo(
        self,
        resultado: ResultadoBusca,
        texto_custo,
        texto_status,
    ):
        if resultado.encontrou:
            texto_custo.set(f"Custo total: {resultado.custo_total:g}")
            texto_status.set("Status: Caminho encontrado")
        else:
            texto_custo.set("Custo total: -")
            texto_status.set("Status: Caminho não encontrado")

    def pausar_comparacao(self):
        if not self.comparacao_em_reproducao or self.comparacao_pausada:
            return

        self.comparacao_pausada = True
        self._cancelar_agendamento()
        self.texto_status_geral.set("Status geral: Comparação pausada")
        self._atualizar_estado_botoes()

    def continuar_comparacao(self):
        if not self.comparacao_em_reproducao or not self.comparacao_pausada:
            return

        self.comparacao_pausada = False
        self.texto_status_geral.set("Status geral: Comparação em andamento")
        self._atualizar_estado_botoes()
        self.executar_proximo_passo_comparacao()

    def executar_um_passo_comparacao(self):
        if not self.comparacao_em_reproducao or not self.comparacao_pausada:
            return

        self._executar_tick_comparacao()

        if self.comparacao_em_reproducao:
            self.texto_status_geral.set("Status geral: Comparação pausada")
            self._atualizar_estado_botoes()

    def reiniciar_comparacao(self):
        self._cancelar_agendamento()
        self.grade_a_estrela.limpar_resultado_busca()
        self.grade_gulosa.limpar_resultado_busca()
        self.grade_a_estrela.definir_edicao_habilitada(False)
        self.grade_gulosa.definir_edicao_habilitada(False)

        self.resultado_a_estrela = None
        self.resultado_gulosa = None
        self.indice_passo_a_estrela = 0
        self.indice_passo_gulosa = 0
        self.indice_caminho_a_estrela = 1
        self.indice_caminho_gulosa = 1
        self.contador_explorados_a_estrela = 0
        self.contador_explorados_gulosa = 0
        self.a_estrela_finalizou = False
        self.gulosa_finalizou = False
        self.comparacao_em_reproducao = False
        self.comparacao_pausada = False

        self.texto_status_geral.set("Status geral: Aguardando")
        self.texto_nos_a_estrela.set("Nós explorados: 0")
        self.texto_custo_a_estrela.set("Custo total: -")
        self.texto_tempo_a_estrela.set("Tempo: -")
        self.texto_status_a_estrela.set("Status: Aguardando")
        self.texto_nos_gulosa.set("Nós explorados: 0")
        self.texto_custo_gulosa.set("Custo total: -")
        self.texto_tempo_gulosa.set("Tempo: -")
        self.texto_status_gulosa.set("Status: Aguardando")
        self.texto_menor_custo.set("Menor custo: -")
        self.texto_menos_nos.set("Menos nós explorados: -")
        self.texto_menor_tempo.set("Menor tempo de cálculo: -")
        self._atualizar_estado_botoes()

    def finalizar_comparacao(self):
        self._cancelar_agendamento()
        self.comparacao_em_reproducao = False
        self.comparacao_pausada = False
        self.texto_status_geral.set("Status geral: Comparação concluída")
        self._atualizar_resumo_final()
        self._atualizar_estado_botoes()

    def _atualizar_resumo_final(self):
        self.texto_menor_custo.set(self._resumir_menor_custo())

        quantidade_a_estrela = len(self.resultado_a_estrela.nos_visitados)
        quantidade_gulosa = len(self.resultado_gulosa.nos_visitados)
        menos_nos = self._comparar_valores(
            quantidade_a_estrela,
            quantidade_gulosa,
        )
        menor_quantidade = min(quantidade_a_estrela, quantidade_gulosa)
        self.texto_menos_nos.set(
            f"Menos nós explorados: {menos_nos} ({menor_quantidade})"
        )

        tempo_a_estrela = self.resultado_a_estrela.tempo_execucao
        tempo_gulosa = self.resultado_gulosa.tempo_execucao
        menor_tempo = self._comparar_valores(
            tempo_a_estrela,
            tempo_gulosa,
        )
        menor_tempo_ms = min(tempo_a_estrela, tempo_gulosa) * 1000
        self.texto_menor_tempo.set(
            f"Menor tempo de cálculo: {menor_tempo} "
            f"({menor_tempo_ms:.3f} ms)"
        )

    def _resumir_menor_custo(self) -> str:
        encontrou_a_estrela = self.resultado_a_estrela.encontrou
        encontrou_gulosa = self.resultado_gulosa.encontrou

        if not encontrou_a_estrela and not encontrou_gulosa:
            return "Menor custo: Nenhum encontrou caminho"

        if encontrou_a_estrela and not encontrou_gulosa:
            custo = self.resultado_a_estrela.custo_total
            return (
                f"Menor custo: A* ({custo:g}; somente A* encontrou caminho)"
            )

        if encontrou_gulosa and not encontrou_a_estrela:
            custo = self.resultado_gulosa.custo_total
            return (
                "Menor custo: Busca Gulosa "
                f"({custo:g}; somente ela encontrou caminho)"
            )

        menor_custo = self._comparar_valores(
            self.resultado_a_estrela.custo_total,
            self.resultado_gulosa.custo_total,
        )
        valor_menor_custo = min(
            self.resultado_a_estrela.custo_total,
            self.resultado_gulosa.custo_total,
        )
        return f"Menor custo: {menor_custo} ({valor_menor_custo:g})"

    def _comparar_valores(self, valor_a_estrela, valor_gulosa) -> str:
        if valor_a_estrela < valor_gulosa:
            return "A*"

        if valor_gulosa < valor_a_estrela:
            return "Busca Gulosa"

        return "Empate"

    def _formatar_tempo(self, tempo_segundos: float) -> str:
        return f"Tempo: {tempo_segundos * 1000:.3f} ms"

    def _atualizar_estado_botoes(self):
        if not hasattr(self, "botao_iniciar"):
            return

        esta_reproduzindo = self.comparacao_em_reproducao
        esta_pausada = self.comparacao_pausada
        possui_resultado = self.resultado_a_estrela is not None

        self.botao_iniciar.configure(
            state="disabled" if esta_reproduzindo else "normal"
        )
        self.botao_pausar.configure(
            state=(
                "normal"
                if esta_reproduzindo and not esta_pausada
                else "disabled"
            )
        )
        self.botao_continuar.configure(
            state="normal" if esta_reproduzindo and esta_pausada else "disabled"
        )
        self.botao_proximo.configure(
            state="normal" if esta_reproduzindo and esta_pausada else "disabled"
        )
        self.botao_reiniciar.configure(
            state="normal" if possui_resultado else "disabled"
        )

    def _alterar_velocidade(self, valor):
        nivel = int(float(valor))
        self.atraso_animacao = converter_nivel_em_atraso(nivel)

    def _obter_nome_heuristica(self) -> str:
        if self.tipo_heuristica == TipoHeuristica.EUCLIDIANA:
            return "Euclidiana"

        if self.tipo_heuristica == TipoHeuristica.DIAGONAL:
            return "Diagonal"

        return "Manhattan"

    def _obter_nome_movimento(self) -> str:
        if self.tipo_movimento == TipoMovimento.OITO_DIRECOES:
            return "8 direções"

        return "4 direções"

    def _cancelar_agendamento(self):
        if self.id_agendamento is not None:
            self.after_cancel(self.id_agendamento)
            self.id_agendamento = None

    def fechar_janela(self):
        self._cancelar_agendamento()
        self.comparacao_em_reproducao = False
        self.destroy()
